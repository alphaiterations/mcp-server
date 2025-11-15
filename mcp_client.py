import subprocess, json, sys, threading, time
from langgraph.graph import StateGraph, END
from typing import TypedDict, Any, Dict
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

# ---------------- LAUNCH MCP SERVER ----------------
server = subprocess.Popen(
    [sys.executable, "mcp_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

print("🔗 Connected to MCP server")

# Read server startup messages (non-blocking)
def read_startup():
    while True:
        line = server.stderr.readline()
        if not line:
            break
        if "Starting MCP server" in line:
            break

startup_thread = threading.Thread(target=read_startup, daemon=True)
startup_thread.start()
time.sleep(1)  # Give server time to start

# ---------------- MCP INITIALIZATION ----------------
request_id = 0

def send_request(method: str, params: Dict = None):
    global request_id
    request_id += 1
    req = {
        "jsonrpc": "2.0",
        "id": str(request_id),
        "method": method,
    }
    if params:
        req["params"] = params
    server.stdin.write(json.dumps(req) + "\n")
    server.stdin.flush()
    return server.stdout.readline().strip()

def send_notification(method: str, params: Dict = None):
    req = {
        "jsonrpc": "2.0",
        "method": method,
    }
    if params:
        req["params"] = params
    server.stdin.write(json.dumps(req) + "\n")
    server.stdin.flush()

# Initialize the MCP connection
print("🔄 Initializing MCP connection...")
init_response = send_request("initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "mcp-client", "version": "1.0.0"}
})
print(f"✅ Initialization response: {init_response}")

# Send initialized notification
send_notification("initialized")
print("✅ MCP connection initialized")

# ---------------- STDIO TOOL CALL ----------------
def call_mcp_tool(tool: str, args: Dict):
    global request_id
    request_id += 1
    req = {
        "jsonrpc": "2.0",
        "id": str(request_id),
        "method": "tools/call",
        "params": {
            "name": tool, 
            "arguments": {"input": args}  # Wrap args in "input" key
        },
    }
    server.stdin.write(json.dumps(req) + "\n")
    server.stdin.flush()
    response = server.stdout.readline().strip()
    try:
        resp_data = json.loads(response)
        if "result" in resp_data:
            return resp_data["result"]
        elif "error" in resp_data:
            return f"Error: {resp_data['error']}"
        return response
    except:
        return response

# ---------------- GRAPH STATE ----------------
class S(TypedDict):
    msg: str
    tool_result: Any
    result: str

# ---------------- AGENT LOGIC ----------------
def route_request(state: S):
    """Use LLM to determine which tool to use and extract parameters"""
    
    # Ask LLM to analyze the request and decide on tool usage
    routing_prompt = f"""Analyze this user request and determine which tool to use:

User request: {state["msg"]}

Available tools:
1. get_weather - Get current weather for a city. Requires: city name
2. web_search - Search the web for information. Requires: search query

Respond in JSON format with:
{{
    "tool": "get_weather" | "web_search" | "none",
    "parameters": {{"city": "..."}} or {{"query": "..."}} or null,
    "reasoning": "brief explanation"
}}

Only use tools if clearly needed. For general conversation, use "none"."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a tool routing assistant. Analyze user requests and determine which tool to use. Always respond with valid JSON."},
            {"role": "user", "content": routing_prompt}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    
    try:
        routing_decision = json.loads(response.choices[0].message.content)
        tool = routing_decision.get("tool")
        params = routing_decision.get("parameters")
        
        print(f"🤖 Routing decision: {routing_decision.get('reasoning')}")
        
        if tool == "get_weather" and params:
            result = call_mcp_tool("get_weather", params)
            return {"msg": state["msg"], "tool_result": result}
        
        elif tool == "web_search" and params:
            result = call_mcp_tool("web_search", params)
            return {"msg": state["msg"], "tool_result": result}
        
        else:
            return {"msg": state["msg"], "tool_result": None}
            
    except Exception as e:
        print(f"⚠️ Routing error: {e}")
        return {"msg": state["msg"], "tool_result": None}

def generate_response(state: S):
    """Use OpenAI to generate a natural language response"""
    if state.get("tool_result") is None:
        # No tool was used, direct LLM response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": state["msg"]}
            ],
            temperature=0.7
        )
        return {
            "msg": state["msg"],
            "tool_result": state.get("tool_result"),
            "result": response.choices[0].message.content
        }
    
    # Format tool result for LLM
    tool_data = json.dumps(state["tool_result"], indent=2)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Use the tool results provided to answer the user's question in a natural, conversational way. Be concise but informative."},
            {"role": "user", "content": f"User question: {state['msg']}\n\nTool results:\n{tool_data}\n\nProvide a helpful answer based on this information. Please limit your answer in 30 words."}
        ],
        temperature=0.7
    )
    
    return {
        "msg": state["msg"],
        "tool_result": state["tool_result"],
        "result": response.choices[0].message.content
    }

# ---------------- BUILD GRAPH ----------------
g = StateGraph(S)
g.add_node("route", route_request)
g.add_node("respond", generate_response)
g.set_entry_point("route")
g.add_edge("route", "respond")
g.add_edge("respond", END)

graph = g.compile()
print("🤖 LangGraph agent ready\n")

# ---------------- TEST ----------------
tests = [
    "What's the weather in Mumbai?",
    "Tell me about the weather in Delhi",
    "Search for latest news about AI",
    "What is Model Context Protocol?"
]

for t in tests:
    print(f"\n{'='*80}")
    print(f"USER: {t}")
    print(f"{'='*80}")
    result = graph.invoke({"msg": t})
    print(f"AGENT: {result['result']}\n")
