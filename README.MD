# 🎯 MCP Server & LangGraph Agent# 🎯 MCP Server & LangGraph Agent



> **Understanding Model Context Protocol (MCP) through a real-world implementation with LangGraph, OpenAI, and live APIs**> **Understanding Model Context Protocol (MCP) through a real-world implementation with LangGraph, OpenAI, and live APIs**



## 🏗️ Architecture Overview## 🎬 The KBC Analogy: Understanding MCP Architecture



This project demonstrates a complete MCP implementation where an LLM intelligently uses external tools to answer user questions. The LLM acts as an intelligent agent that recognizes when it needs specialized knowledge and orchestrates calls to appropriate tools.Imagine **Kaun Banega Crorepati (KBC)**. Here's how the game maps perfectly to MCP:



```### The Cast & Their Roles

┌─────────────────────────────────────────────────────────┐

│                         USER                            │| KBC Element | MCP Component | What They Do |

│              Asks: "Weather in Mumbai?"                 │|-------------|---------------|--------------|

└─────────────────────┬───────────────────────────────────┘| **�️ Computer Ji (Question Source)** | **User** | Presents questions that need answers |

                      │| **🎙️ Amitabh Bachchan (The Host)** | **MCP Host (LangGraph)** | Orchestrates the game, manages lifelines, facilitates the flow |

                      ▼| **🧑‍💼 The Contestant** | **LLM (OpenAI GPT-4o-mini)** | Tries to answer questions, decides when to use lifelines, gives final answers |

┌─────────────────────────────────────────────────────────┐| **📞 Phone-a-Friend System** | **MCP Client (Protocol)** | Communication infrastructure to reach experts |

│                    MCP HOST                             │| **👥 Expert Friends** | **MCP Server Tools** | Domain specialists (Weather Expert, Google Expert, etc.) |

│              LangGraph Orchestration                     │

│  • Manages workflow state                               │### 🎯 How It Works

│  • Coordinates LLM and tool interactions                │

│  • Routes requests through the pipeline                 │```

└─────────────────────┬───────────────────────────────────┘Computer Ji: "What's the weather in Mumbai?"

                      │          ↓

                      ▼Amitabh (Host):

┌─────────────────────────────────────────────────────────┐  - Reads question to contestant

│              LLM (GPT-4o-mini)                          │  - "You can use your lifelines if needed"

│  ┌─────────────────────────────────────────────────┐   │          ↓

│  │  Route Node: Analyzes query and decides        │   │Contestant (LLM):

│  │  which tool to use (if any)                     │   │  - Thinks: "I don't have real-time weather data"

│  └─────────────────────┬───────────────────────────┘   │  - Decides: "I need to use Phone-a-Friend!"

│                        │ Requests tool execution        │  - "Amitabh ji, I want to use my Phone-a-Friend lifeline"

│                        ▼                                │          ↓

│  ┌─────────────────────────────────────────────────┐   │Amitabh (Host):

│  │  Respond Node: Formats tool results into       │   │  - "Sure! Let me connect you to the Weather Expert"

│  │  natural language response                      │   │  - Orchestrates the lifeline activation

│  └─────────────────────────────────────────────────┘   │          ↓

└─────────────────────┬───────────────────────────────────┘Phone System (MCP Protocol):

                      │  - Dials the Weather Expert

                      │ Uses MCP Protocol  - Transmits: "What's the weather in Mumbai?"

                      ▼  - Waits for response

┌─────────────────────────────────────────────────────────┐          ↓

│         MCP CLIENT (Protocol Layer)                     │Weather Expert Friend (MCP Tool):

│  • JSON-RPC 2.0 Implementation                          │  - Calls wttr.in API

│  • STDIO Communication                                  │  - Returns: "31°C, Sunny, 26% humidity"

│  • Request/Response Handling                            │          ↓

└─────────────────────┬───────────────────────────────────┘Phone System (MCP Protocol):

                      │  - Delivers data back to contestant

                      │ MCP Protocol (JSON-RPC over STDIO)          ↓

                      │Contestant (LLM):

                      ▼  - Receives: "31°C, Sunny, 26% humidity"

┌─────────────────────────────────────────────────────────┐  - Formulates answer: "Based on my friend's input..."

│              MCP SERVER (Tools)                         │  - "Mumbai is experiencing sunny weather at 31°C!"

│  ┌─────────────────────────────────────────────────┐   │          ↓

│  │  📍 get_weather(city)                           │   │Amitabh (Host):

│  │     └─▶ Calls wttr.in API                       │   │  - "Contestant ne kaha Mumbai is experiencing sunny weather..."

│  │                                                  │   │  - "Computer ji, lock kiya jaye?"

│  │  🔍 web_search(query)                           │   │          ↓

│  │     └─▶ Calls Serper API (Google Search)        │   │Computer Ji: Locks the answer and shows result

│  └─────────────────────────────────────────────────┘   │```

└─────────────────────────────────────────────────────────┘

```**The Key Insight:** 

- The **Contestant (LLM)** doesn't know everything - it recognizes when it needs help

### Key Components- **Amitabh (MCP Host)** doesn't answer questions - he orchestrates and facilitates

- **Phone-a-Friend (MCP)** provides access to specialized knowledge the contestant lacks

| Component | Description | Role |- **Computer Ji (User)** asks questions and validates answers

|-----------|-------------|------|

| **User** | Question source | Initiates queries |This is exactly how MCP works - the LLM recognizes its limitations and uses tools as lifelines!

| **MCP Host** | LangGraph workflow | Orchestrates the entire process |

| **LLM** | OpenAI GPT-4o-mini | Makes intelligent routing decisions and formats responses |---

| **MCP Client** | Protocol implementation | Handles JSON-RPC communication via STDIO |

| **MCP Server** | Tool provider | Exposes specialized tools (weather, web search) |## 🏗️ Architecture Overview



---```

┌─────────────────────────────────────────────────────────┐

## 🚀 Quick Start│              COMPUTER JI (User)                         │

│              Asks: "Weather in Mumbai?"                 │

### Prerequisites└─────────────────────┬───────────────────────────────────┘

                      │

- Python 3.8+                      ▼

- OpenAI API Key┌─────────────────────────────────────────────────────────┐

- Serper API Key (for web search)│         AMITABH BACHCHAN (MCP Host)                     │

│              LangGraph Orchestration                     │

### Installation│  • Presents question to contestant                      │

│  • Manages lifeline activation                          │

```bash│  • Facilitates the game flow                            │

# Clone the repository└─────────────────────┬───────────────────────────────────┘

git clone <your-repo-url>                      │

cd mcp-server                      ▼

┌─────────────────────────────────────────────────────────┐

# Create virtual environment│         THE CONTESTANT (LLM - GPT-4o-mini)              │

python -m venv .venv│  ┌─────────────────────────────────────────────────┐   │

source .venv/bin/activate  # On Windows: .venv\Scripts\activate│  │  Route Node: "I need Phone-a-Friend!"           │   │

│  │  (Decides which expert to call)                  │   │

# Install dependencies│  └─────────────────────┬───────────────────────────┘   │

pip install -r requirements.txt│                        │ Requests lifeline              │

```│                        ▼                                │

│  ┌─────────────────────────────────────────────────┐   │

### Configuration│  │  Respond Node: Formulates final answer          │   │

│  │  (After receiving expert's input)                │   │

Create a `.env` file:│  └─────────────────────────────────────────────────┘   │

└─────────────────────┬───────────────────────────────────┘

```properties                      │

OPEN_AI_KEY=sk-your-openai-api-key                      │ Uses Phone-a-Friend

SERPER_API_KEY=your-serper-api-key                      ▼

```┌─────────────────────────────────────────────────────────┐

│      PHONE SYSTEM (MCP Client - Protocol Layer)        │

### Run the Agent│  • JSON-RPC 2.0 Implementation                          │

│  • STDIO Communication                                  │

```bash│  • Connects contestant to expert friends                │

python mcp_client.py└─────────────────────┬───────────────────────────────────┘

```                      │

                      │ MCP Protocol (JSON-RPC over STDIO)

---                      │

                      ▼

## 📝 What This Demo Does┌─────────────────────────────────────────────────────────┐

│         EXPERT FRIENDS (MCP Server Tools)               │

The system demonstrates a complete MCP implementation with:│  ┌─────────────────────────────────────────────────┐   │

│  │  📍 Weather Expert - get_weather(city)          │   │

1. **Intelligent Tool Routing** - LLM analyzes user queries and decides which tool to use│  │     └─▶ Calls wttr.in API                       │   │

2. **Real Weather Data** - Fetches live weather via wttr.in API│  │                                                  │   │

3. **Web Search** - Google search results via Serper API│  │  🔍 Google Expert - web_search(query)           │   │

4. **Natural Language Responses** - GPT-4o-mini formats tool results into conversational answers│  │     └─▶ Calls Serper API                        │   │

│  └─────────────────────────────────────────────────┘   │

### Example Interactions└─────────────────────────────────────────────────────────┘

```

```

USER: What's the weather in Mumbai?---



🤖 Routing decision: The user is asking for weather, using get_weather tool## 🚀 Quick Start



AGENT: Mumbai is experiencing sunny weather at 31°C (88°F). The humidity ### Prerequisites

       is at 26% with light winds at 9 km/h. It feels slightly warmer 

       at around 33°C.- Python 3.8+

```- OpenAI API Key

- Serper API Key (for web search)

```

USER: Search for latest news about AI### Installation



🤖 Routing decision: User needs web search for latest information```bash

# Clone the repository

AGENT: Here are the latest AI news articles:git clone <your-repo-url>

       cd mcp-server

       1. **TechCrunch - AI News & Analysis**

          Coverage of the latest developments in AI and machine learning# Create virtual environment

       python -m venv .venv

       2. **WSJ - Artificial Intelligence Updates**source .venv/bin/activate  # On Windows: .venv\Scripts\activate

          Investment trends and corporate AI initiatives

       # Install dependencies

       3. **MIT News - AI Research**pip install -r requirements.txt

          Latest breakthroughs from MIT's AI labs```

       

       [Additional results with links and snippets...]### Configuration

```

Create a `.env` file:

---

```properties

## 🔧 Technical Deep DiveOPEN_AI_KEY=sk-your-openai-api-key

SERPER_API_KEY=your-serper-api-key

### 1. MCP Server (`mcp_server.py`)```



The server exposes tools using FastMCP:### Run the Agent



```python```bash

from fastmcp import FastMCPpython mcp_client.py

from pydantic import BaseModel```



mcp = FastMCP("multi-tool-server")---



class WeatherInput(BaseModel):## 📝 What This Demo Does

    city: str

The system demonstrates a complete MCP implementation with:

@mcp.tool()

def get_weather(input: WeatherInput):1. **Intelligent Tool Routing** - LLM analyzes user queries and decides which tool to use

    """Get current weather for a city using wttr.in API"""2. **Real Weather Data** - Fetches live weather via wttr.in API

    url = f"https://wttr.in/{input.city}?format=j1"3. **Web Search** - Google search results via Serper API

    response = requests.get(url, timeout=5)4. **Natural Language Responses** - GPT-4o-mini formats tool results into conversational answers

    # Parse and return structured weather data

    return weather_info### Example Interactions



class WebSearchInput(BaseModel):```

    query: strCOMPUTER JI: What's the weather in Mumbai?

              ↓

@mcp.tool()AMITABH: "Chaliye contestant, aapka sawal hai..."

def web_search(input: WebSearchInput):              ↓

    """Search the web using Serper API"""CONTESTANT (LLM): 

    # Call Serper Google Search API🤖 Routing decision: I need the weather expert's help!

    # Return top results with titles, links, and snippets              ↓

    return search_resultsAMITABH: "Phone-a-Friend activated!"

```              ↓

[Phone connects to Weather Expert]

**Responsibilities:**              ↓

- Tool implementation and business logicCONTESTANT (LLM): 

- External API integration (wttr.in, Serper)AGENT: Mumbai is experiencing sunny weather at 31°C (88°F). 

- Input validation using Pydantic models       The humidity is at 26% with light winds at 9 km/h...

- Error handling and response formatting              ↓

AMITABH: "Computer ji, lock kiya jaye?"

---```



### 2. MCP Client (`mcp_client.py` - Protocol Layer)```

COMPUTER JI: Search for latest news about AI

Implements the MCP protocol specification:              ↓

AMITABH: "Yeh sawal contestant ke liye..."

```python              ↓

# Initialize MCP connectionCONTESTANT (LLM): 

def send_request(method: str, params: Dict):🤖 Routing decision: I need the Google Expert!

    """Send JSON-RPC request to MCP server"""              ↓

    req = {[Phone connects to Google Expert]

        "jsonrpc": "2.0",              ↓

        "id": str(request_id),CONTESTANT (LLM):

        "method": method,AGENT: Here are the latest AI news articles:

        "params": params       1. TechCrunch - AI News & Analysis

    }       2. WSJ - Artificial Intelligence Updates

    server.stdin.write(json.dumps(req) + "\n")       ...

    return server.stdout.readline().strip()```



# MCP initialization handshake---

send_request("initialize", {

    "protocolVersion": "2024-11-05",## 🔧 Technical Deep Dive

    "capabilities": {},

    "clientInfo": {"name": "mcp-client", "version": "1.0.0"}### 1. MCP Server (`mcp_server.py`)

})

send_notification("initialized")The server exposes tools using FastMCP:



# Tool invocation```python

def call_mcp_tool(tool: str, args: Dict):from fastmcp import FastMCP

    """Call an MCP tool via JSON-RPC"""

    req = {mcp = FastMCP("multi-tool-server")

        "jsonrpc": "2.0",

        "method": "tools/call",@mcp.tool()

        "params": {def get_weather(input: WeatherInput):

            "name": tool,    """Get current weather for a city"""

            "arguments": {"input": args}    url = f"https://wttr.in/{input.city}?format=j1"

        }    response = requests.get(url, timeout=5)

    }    # Returns structured weather data

    # Send via STDIO and parse response

```@mcp.tool()

def web_search(input: WebSearchInput):

**Responsibilities:**    """Search the web using Serper API"""

- JSON-RPC 2.0 protocol implementation    # Calls Google Search API

- STDIO-based communication with server subprocess    # Returns top results with snippets

- Request/response lifecycle management```

- Connection initialization and capability negotiation

**Responsibilities:**

---- Tool implementation

- API integration

### 3. MCP Host (`mcp_client.py` - Application Layer)- Input validation

- Error handling

LangGraph orchestration with LLM intelligence:

### 2. MCP Client (`mcp_client.py` - Protocol Layer)

```python

from langgraph.graph import StateGraph, ENDImplements MCP protocol specification:

from openai import OpenAI

```python

client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))# Initialize MCP connection

def send_request(method: str, params: Dict):

# Define workflow state    req = {

class S(TypedDict):        "jsonrpc": "2.0",

    msg: str        "id": str(request_id),

    tool_result: Any        "method": method,

    result: str        "params": params

    }

# Node 1: Intelligent routing    server.stdin.write(json.dumps(req) + "\n")

def route_request(state: S):    return server.stdout.readline().strip()

    """LLM analyzes query and decides which tool to use"""

    routing_prompt = f"""Analyze this user request and determine which tool to use:# Initialization handshake

    send_request("initialize", {

    User request: {state["msg"]}    "protocolVersion": "2024-11-05",

        "capabilities": {},

    Available tools:    "clientInfo": {"name": "mcp-client", "version": "1.0.0"}

    1. get_weather - Get current weather for a city})

    2. web_search - Search the web for informationsend_notification("initialized")

    

    Respond in JSON format with tool selection and parameters."""# Tool calling

    def call_mcp_tool(tool: str, args: Dict):

    response = client.chat.completions.create(    req = {

        model="gpt-4o-mini",        "method": "tools/call",

        messages=[{        "params": {"name": tool, "arguments": {"input": args}}

            "role": "system",    }

            "content": "You are a tool routing assistant."    # Send and receive via STDIO

        }, {```

            "role": "user",

            "content": routing_prompt**Responsibilities:**

        }],- JSON-RPC protocol implementation

        response_format={"type": "json_object"}- STDIO communication

    )- Request/response handling

    - Connection lifecycle management

    routing_decision = json.loads(response.choices[0].message.content)

    ### 3. MCP Host (`mcp_client.py` - Application Layer)

    # Call the appropriate tool

    if routing_decision["tool"] == "get_weather":LangGraph orchestration with LLM intelligence:

        result = call_mcp_tool("get_weather", routing_decision["parameters"])

    elif routing_decision["tool"] == "web_search":```python

        result = call_mcp_tool("web_search", routing_decision["parameters"])# Define workflow state

    class S(TypedDict):

    return {"msg": state["msg"], "tool_result": result}    msg: str

    tool_result: Any

# Node 2: Response generation    result: str

def generate_response(state: S):

    """LLM formats tool results into natural language"""# Intelligent routing node

    response = client.chat.completions.create(def route_request(state: S):

        model="gpt-4o-mini",    """LLM decides which tool to use"""

        messages=[{    response = client.chat.completions.create(

            "role": "system",        model="gpt-4o-mini",

            "content": "Format the tool results into a natural, helpful response."        messages=[{

        }, {            "role": "system",

            "role": "user",            "content": "Analyze and decide which tool to use..."

            "content": f"Question: {state['msg']}\n\nTool results: {state['tool_result']}"        }],

        }]        response_format={"type": "json_object"}

    )    )

        # LLM returns: {"tool": "get_weather", "parameters": {"city": "Mumbai"}}

    return {    

        "msg": state["msg"],# Response generation node

        "tool_result": state["tool_result"],def generate_response(state: S):

        "result": response.choices[0].message.content    """LLM formats tool results into natural language"""

    }    response = client.chat.completions.create(

        model="gpt-4o-mini",

# Build LangGraph workflow        messages=[{

g = StateGraph(S)            "role": "user",

g.add_node("route", route_request)            "content": f"Tool results: {tool_data}\nProvide helpful answer"

g.add_node("respond", generate_response)        }]

g.set_entry_point("route")    )

g.add_edge("route", "respond")    

g.add_edge("respond", END)# Build LangGraph

g = StateGraph(S)

graph = g.compile()g.add_node("route", route_request)

```g.add_node("respond", generate_response)

g.add_edge("route", "respond")

**Responsibilities:**graph = g.compile()

- Workflow orchestration via LangGraph```

- LLM integration for intelligent decision-making

- Tool routing based on query analysis**Responsibilities:**

- Natural language response generation- Workflow orchestration (like Amitabh managing the game)

- State management across workflow nodes- Connects LLM (contestant) with tools (expert friends)

- Manages the overall game flow

---- Presents questions and final answers



## 🎯 Key MCP Concepts Demonstrated---



### 1. Protocol Standardization## 🎯 Key MCP Concepts Demonstrated

- **JSON-RPC 2.0 format** - Standard request/response structure

- **Standard method names** - `initialize`, `tools/call`, `tools/list`### 1. **Protocol Standardization**

- **Capability negotiation** - Client and server exchange supported features- JSON-RPC 2.0 format

- **Version compatibility** - Protocol version: `2024-11-05`- Standard method names (`initialize`, `tools/call`)

- Capability negotiation

### 2. Transport Flexibility

- **Current**: STDIO (standard input/output streams)### 2. **Transport Flexibility**

- **Alternatives**: HTTP/SSE, WebSockets- Currently: STDIO (standard input/output)

- **Key Point**: Protocol remains the same regardless of transport- Could be: HTTP/SSE, WebSockets

- Protocol stays the same

### 3. Tool Discovery & Invocation

- Server exposes tools via `@mcp.tool()` decorator### 3. **Tool Discovery & Invocation**

- Client discovers available tools dynamically- Server exposes tools via `@mcp.tool()` decorator

- Type-safe tool definitions using Pydantic- Client discovers and calls tools dynamically

- Structured input/output validation- Type-safe with Pydantic models



### 4. Separation of Concerns### 4. **Separation of Concerns**

- **Server**: Tool implementation, external integrations- **Server**: Tool implementation, API integration

- **Client**: Protocol communication, connection management- **Client**: Protocol communication

- **Host**: AI orchestration, user experience, workflow logic- **Host**: AI orchestration, user experience



------



## 🔄 Complete Request Flow## 🔄 Request Flow Example



Here's what happens when a user asks: *"What's the weather in Mumbai?"*```python

# Computer Ji asks a question

```pythonuser_query = "What's the weather in Mumbai?"

# STEP 1: User initiates query

user_query = "What's the weather in Mumbai?"# ====== STEP 1: Amitabh presents to Contestant ======

state = {"msg": user_query}state = {"msg": user_query}

result = graph.invoke(state)result = graph.invoke(state)



# STEP 2: LangGraph routes to route_request node# ====== STEP 2: Contestant (LLM) Analyzes in route_request() ======

# LLM analyzes the query# Contestant thinks: "I don't have real-time weather data!"

response = client.chat.completions.create(# Contestant decides: "I need Phone-a-Friend - Weather Expert!"

    model="gpt-4o-mini",response = client.chat.completions.create(

    messages=[{"content": "Which tool should I use for this query?"}]    model="gpt-4o-mini",

)    messages=[{"content": "Which tool should I use?"}]

# LLM decides: {"tool": "get_weather", "parameters": {"city": "Mumbai"}})

# LLM returns: {"tool": "get_weather", "parameters": {"city": "Mumbai"}}

# STEP 3: MCP Host calls the tool via MCP Client

call_mcp_tool("get_weather", {"city": "Mumbai"})# ====== STEP 3: Amitabh activates Phone-a-Friend ======

# Calls call_mcp_tool("get_weather", {"city": "Mumbai"})

# STEP 4: MCP Client formats JSON-RPC request

{# ====== STEP 4: Phone System (MCP Client) Dials ======

    "jsonrpc": "2.0",# Creates JSON-RPC request:

    "id": "5",{

    "method": "tools/call",    "jsonrpc": "2.0",

    "params": {    "id": "5",

        "name": "get_weather",    "method": "tools/call",

        "arguments": {"input": {"city": "Mumbai"}}    "params": {

    }        "name": "get_weather",

}        "arguments": {"input": {"city": "Mumbai"}}

# Sends to server via subprocess stdin    }

}

# STEP 5: MCP Server receives and executes# Sends via server.stdin → subprocess

# FastMCP routes to get_weather() function

# Calls wttr.in API# ====== STEP 5: Weather Expert Friend (MCP Server) ======

# Returns structured weather data:# FastMCP receives request, executes get_weather()

{# Calls wttr.in API

    "jsonrpc": "2.0",# Returns JSON-RPC response:

    "id": "5",{

    "result": {    "jsonrpc": "2.0",

        "content": [{    "id": "5",

            "type": "text",    "result": {

            "text": '{"temperature": "31°C", "condition": "Sunny", ...}'        "content": [{

        }]            "type": "text",

    }            "text": '{"temperature": "31°C", "condition": "Sunny", ...}'

}        }]

    }

# STEP 6: MCP Client parses response}

# Extracts result and returns to Host

# ====== STEP 6: Phone System returns to Contestant ======

# STEP 7: LangGraph routes to generate_response node# Parses response, delivers to LLM

# LLM receives tool result and formats response

response = client.chat.completions.create(# ====== STEP 7: Contestant formulates answer in generate_response() ======

    model="gpt-4o-mini",# Contestant receives friend's data

    messages=[{# Contestant crafts natural language response:

        "content": f"User asked: {user_query}\nTool returned: {tool_data}\nProvide helpful answer"response = client.chat.completions.create(

    }]    model="gpt-4o-mini",

)    messages=[{

# Returns: "Mumbai is experiencing sunny weather at 31°C..."        "role": "user",

        "content": f"Based on tool results: {tool_data}, answer the question"

# STEP 8: Final response returned to user    }]

```)

# Returns: "Mumbai is experiencing sunny weather at 31°C..."

---

# ====== STEP 8: Amitabh presents final answer ======

## 📚 File Structure# "Computer ji, lock kiya jaye?"

# Final result returned to user

``````

mcp-server/

├── mcp_server.py          # MCP Server - Tool implementations---

├── mcp_client.py          # MCP Client + Host - Protocol & LangGraph

├── requirements.txt       # Python dependencies## 📚 File Structure

├── .env                   # API keys (gitignored)

├── README.md             # Documentation```

└── .gitignoremcp-server/

```├── mcp_server.py          # MCP Server (Tools implementation)

├── mcp_client.py          # MCP Client + Host (Protocol + LangGraph)

---├── requirements.txt       # Python dependencies

├── .env                   # API keys (not in git)

## 🛠️ Technologies Used├── README.md             # This file

└── .gitignore

| Technology | Purpose |```

|------------|---------|

| **FastMCP** | MCP server framework |---

| **LangGraph** | Workflow orchestration |

| **OpenAI GPT-4o-mini** | LLM for intelligent routing and response generation |## 🛠️ Technologies Used

| **Serper API** | Google web search |

| **wttr.in** | Weather data API |- **FastMCP** - MCP server framework

| **Pydantic** | Type validation and data modeling |- **LangGraph** - Workflow orchestration

| **Python STDIO** | Inter-process communication |- **OpenAI GPT-4o-mini** - LLM for routing and response generation

- **Serper API** - Web search

---- **wttr.in** - Weather data

- **Pydantic** - Type validation

## 🎓 Learning Resources

---

### MCP (Model Context Protocol)

- [Official MCP Documentation](https://modelcontextprotocol.io/)## 🎓 Learning Resources

- [MCP Specification](https://spec.modelcontextprotocol.io/)

- [FastMCP Framework](https://github.com/jlowin/fastmcp)### MCP Documentation

- [Anthropic's MCP Introduction](https://www.anthropic.com/news/model-context-protocol)- [Model Context Protocol Docs](https://modelcontextprotocol.io/)

- [FastMCP Framework](https://github.com/jlowin/fastmcp)

### LangGraph & LangChain- [MCP Specification](https://spec.modelcontextprotocol.io/)

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

- [LangChain MCP Adapters](https://github.com/rectalogic/langchain-mcp-adapters)### LangGraph

- [Building Agentic Workflows](https://python.langchain.com/docs/langgraph)- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

- [LangChain MCP Adapters](https://github.com/rectalogic/langchain-mcp-adapters)

---

---

## 🔮 Extending This Project

## 🔮 Extending This Project

### Add More Tools

### Add More Tools

```python

# In mcp_server.py```python

# In mcp_server.py

@mcp.tool()@mcp.tool()

def get_stock_price(input: StockInput):def calculate(input: CalculationInput):

    """Get real-time stock prices from financial API"""    """Perform mathematical calculations"""

    # Integrate with Alpha Vantage, Yahoo Finance, etc.    return eval(input.expression)  # Be careful with eval!

    return stock_data

@mcp.tool()

@mcp.tool()def get_stock_price(input: StockInput):

def summarize_document(input: DocumentInput):    """Get real-time stock prices"""

    """Summarize a document using AI"""    # Call financial API

    # Call OpenAI API for summarization```

    return summary

### Use Different Transport

@mcp.tool()

def query_database(input: SQLInput):```python

    """Execute SQL queries on database"""# For HTTP/SSE instead of STDIO

    # Safe SQL execution with validationif __name__ == "__main__":

    return results    import uvicorn

```    uvicorn.run(mcp.sse_app(), host="127.0.0.1", port=8000)

```

### Switch to HTTP/SSE Transport

### Add Memory/Context

```python

# In mcp_server.py```python

if __name__ == "__main__":# Add conversation history to LangGraph state

    import uvicornclass S(TypedDict):

    # Use SSE (Server-Sent Events) instead of STDIO    msg: str

    uvicorn.run(mcp.sse_app(), host="127.0.0.1", port=8000)    history: List[Dict]  # Chat history

```    tool_result: Any

    result: str

### Add Conversation Memory```



```python---

# Extend state to include chat history

class S(TypedDict):## ⚠️ Important Notes

    msg: str

    history: List[Dict]  # Previous messages### Security Considerations

    tool_result: Any- Never commit `.env` file with API keys

    result: str- Validate all tool inputs

- Be cautious with tool execution permissions

def route_request(state: S):- Use rate limiting for API calls

    # Use conversation history for context

    context = "\n".join([f"{m['role']}: {m['content']}" ### API Costs

                         for m in state.get("history", [])])- OpenAI API calls cost money (GPT-4o-mini is cheap but not free)

    # Include in LLM prompt for better understanding- Serper API has free tier limits

```- Monitor your usage



### Implement Caching### Error Handling

- Network failures (API timeouts)

```python- Invalid tool parameters

from functools import lru_cache- LLM hallucinations (wrong tool selection)

- Rate limits

@lru_cache(maxsize=100)

def cached_tool_call(tool: str, args_json: str):---

    """Cache tool results to reduce API calls"""

    args = json.loads(args_json)## 🤝 Contributing

    return call_mcp_tool(tool, args)

```Feel free to:

- Add new tools

---- Improve error handling

- Enhance the LLM prompts

## ⚠️ Important Notes- Add conversation memory

- Implement caching

### Security Considerations

- **Never commit `.env` file** - Contains sensitive API keys---

- **Validate all tool inputs** - Use Pydantic models for type safety

- **Limit tool permissions** - Restrict what tools can access## 📄 License

- **Rate limiting** - Implement to prevent API abuse

- **Input sanitization** - Especially for tools that execute code or queriesMIT License



### API Costs & Limits---

- **OpenAI GPT-4o-mini** - ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens

- **Serper API** - Free tier: 2,500 searches/month## 🙏 Acknowledgments

- **wttr.in** - Free, no API key required

- **Monitor usage** - Set up billing alerts- [Anthropic](https://anthropic.com) for creating the MCP specification

- [FastMCP](https://github.com/jlowin/fastmcp) for the excellent framework

### Error Handling Best Practices- [LangChain](https://langchain.com) for LangGraph

- Network failures and timeouts- Amitabh Bachchan for inspiring the analogy 🎬

- Invalid tool parameters

- LLM hallucinations (wrong tool selection)---

- API rate limit errors

- Malformed JSON-RPC responses**Built with ❤️ to demonstrate the power of Model Context Protocol**


---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Add more MCP tools
- Improve error handling and retry logic
- Enhance LLM prompts for better routing
- Add conversation memory and context
- Implement response caching
- Add unit and integration tests
- Support additional transport protocols
- Create web UI for interactions

---

## 📄 License

MIT License - Feel free to use this project for learning and experimentation.

---

## 🙏 Acknowledgments

- **Anthropic** - For creating the Model Context Protocol specification
- **FastMCP** - For the excellent Python MCP framework
- **LangChain Team** - For LangGraph and ecosystem tools
- **OpenAI** - For GPT models and API
- **Serper** - For web search API
- **wttr.in** - For free weather data

---

**Built with ❤️ to demonstrate the power of Model Context Protocol**

*Last updated: November 2025*
