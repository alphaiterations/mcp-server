# MCP Server with LangGraph Agent

Read Complete Medium Article here : [Building an AI Agent with Model Context Protocol (MCP): A Complete Guide](https://medium.com/@alphaiterations/building-an-ai-agent-with-model-context-protocol-mcp-a-complete-guide-37b8f6cd7b2b)

## 📖 Overview

This project demonstrates a complete implementation of the **Model Context Protocol (MCP)** with an intelligent agent built using **LangGraph** and **OpenAI**. The system enables AI applications to seamlessly interact with external tools through a standardized protocol.

## 🧩 What is MCP (Model Context Protocol)?

**Model Context Protocol (MCP)** is an open protocol that standardizes how applications provide context to Large Language Models (LLMs). Think of it as a universal adapter that allows AI applications to:

- 🔌 Connect to external data sources and tools
- 🛠️ Execute actions in a standardized way
- 🔄 Maintain consistent communication patterns
- 🌐 Enable tool interoperability across different AI systems

### Key Concepts

1. **MCP Server**: Exposes tools/capabilities that can be called by clients
2. **MCP Client**: Consumes tools from MCP servers
3. **JSON-RPC Protocol**: Communication standard for request/response patterns
4. **Tools**: Individual capabilities exposed by the server (e.g., weather, web search)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INPUT                            │
│                 "What's the weather in Mumbai?"              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   LANGGRAPH AGENT                            │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │   Routing    │────────▶│   Response   │                  │
│  │     Node     │         │    Node      │                  │
│  └──────┬───────┘         └──────────────┘                  │
│         │                                                     │
│         │ Uses OpenAI to determine:                          │
│         │ - Which tool to use                                │
│         │ - Extract parameters                               │
└─────────┼─────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP CLIENT                                │
│  - Manages connection to MCP server                          │
│  - Sends JSON-RPC requests                                   │
│  - Receives and processes responses                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ JSON-RPC over STDIO
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP SERVER                                │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │ get_weather  │         │  web_search  │                  │
│  │    Tool      │         │     Tool     │                  │
│  └──────────────┘         └──────────────┘                  │
│                                                               │
│  Built with FastMCP framework                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   EXTERNAL APIs                              │
│  • wttr.in (Weather API)                                     │
│  • Serper API (Web Search)                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Complete Flow Explanation

### 1. **System Initialization**

```python
# mcp_client.py starts the MCP server as a subprocess
server = subprocess.Popen(
    [sys.executable, "mcp_server.py"],
    stdin=subprocess.PIPE,    # For sending requests
    stdout=subprocess.PIPE,   # For receiving responses
    stderr=subprocess.PIPE,   # For server logs
    text=True
)
```

**What happens:**
- Client spawns the MCP server as a child process
- Communication happens via STDIO (standard input/output)
- JSON-RPC messages flow through pipes

### 2. **MCP Handshake**

```python
# Client sends initialization request
send_request("initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "mcp-client", "version": "1.0.0"}
})

# Client sends initialized notification
send_notification("initialized")
```

**What happens:**
- Client and server negotiate protocol version
- Server confirms available capabilities
- Connection is established and ready for tool calls

### 3. **User Request Processing**

#### Step 3.1: User Input
```
User: "What's the weather in Mumbai?"
```

#### Step 3.2: LangGraph Routing Node
The routing node uses **OpenAI GPT-4** to analyze the request:

```python
def route_request(state):
    # LLM analyzes the user request
    # Determines: tool="get_weather", parameters={"city": "Mumbai"}
    result = call_mcp_tool("get_weather", {"city": "Mumbai"})
    return {"tool_result": result}
```

**What happens:**
- OpenAI analyzes the user's natural language
- Determines which tool is needed
- Extracts parameters from the request
- Routes to appropriate tool

#### Step 3.3: MCP Tool Call
```python
# Client sends JSON-RPC request to server
{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
        "name": "get_weather",
        "arguments": {"input": {"city": "Mumbai"}}
    }
}
```

**What happens:**
- Client formats request in JSON-RPC standard
- Sends to server via stdin
- Waits for response on stdout

#### Step 3.4: MCP Server Execution
```python
@mcp.tool()
def get_weather(input: WeatherInput):
    url = f"https://wttr.in/{input.city}?format=j1"
    response = requests.get(url)
    # Process and return weather data
```

**What happens:**
- Server receives tool call
- Executes the `get_weather` function
- Calls external weather API
- Returns structured data

#### Step 3.5: Response Generation
```python
def generate_response(state):
    # Uses OpenAI to convert tool data into natural language
    # Input: Raw weather data
    # Output: "The current weather in Mumbai is 28°C with clear skies..."
```

**What happens:**
- Raw tool data is formatted for the LLM
- OpenAI generates a natural, conversational response
- User receives friendly answer

---

## 🛠️ Available Tools

### 1. Weather Tool (`get_weather`)
- **Purpose**: Get current weather for any city
- **API**: wttr.in (free, no API key needed)
- **Input**: `{"city": "CityName"}`
- **Output**: Temperature, condition, humidity, wind speed

**Example:**
```python
Input:  {"city": "Mumbai"}
Output: {
    "location": "Mumbai, India",
    "temperature": "28°C / 82°F",
    "condition": "Partly cloudy",
    "humidity": "70%",
    "wind": "15 km/h"
}
```

### 2. Web Search Tool (`web_search`)
- **Purpose**: Search the web for information
- **API**: Serper API (requires API key)
- **Input**: `{"query": "search terms"}`
- **Output**: Top 5 search results with titles, links, snippets

**Example:**
```python
Input:  {"query": "latest news about AI"}
Output: {
    "query": "latest news about AI",
    "results": [
        {
            "title": "AI Breakthrough...",
            "link": "https://...",
            "snippet": "..."
        }
    ]
}
```

---

## 📦 Project Structure

```
mcp-server/
├── mcp_server.py           # MCP server implementation (FastMCP)
├── mcp_client.py           # MCP client + LangGraph agent
├── mcp-server.ipynb        # Jupyter notebook for testing
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
└── README.md              # This file
```

### File Descriptions

**`mcp_server.py`**
- Implements the MCP server using FastMCP framework
- Defines tools with `@mcp.tool()` decorator
- Handles JSON-RPC requests
- Interfaces with external APIs

**`mcp_client.py`**
- Spawns and manages MCP server process
- Implements JSON-RPC client communication
- Builds LangGraph agent with routing logic
- Orchestrates OpenAI for intelligent routing and responses

**`requirements.txt`**
- Lists all Python dependencies
- Includes MCP, LangGraph, OpenAI, and utilities

---

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd mcp-server
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:

```env
# OpenAI API Key (required)
OPEN_AI_KEY=your_openai_api_key_here

# Serper API Key (required for web search)
SERPER_API_KEY=your_serper_api_key_here

# OpenWeather API Key (optional, using free wttr.in instead)
OPENWEATHER_API_KEY=
```

**Getting API Keys:**
- **OpenAI**: https://platform.openai.com/api-keys
- **Serper**: https://serper.dev/ (free tier available)

### 4. Run the System
```bash
python mcp_client.py
```

---

## 💡 How It Works: Step-by-Step Example

### Example: "What's the weather in Mumbai?"

**Step 1: User Input**
```
User enters: "What's the weather in Mumbai?"
```

**Step 2: LangGraph Routing**
```
LLM analyzes → Determines tool: get_weather
             → Extracts parameter: city = "Mumbai"
```

**Step 3: MCP Communication**
```
Client → Server: {
    "method": "tools/call",
    "params": {"name": "get_weather", "arguments": {"input": {"city": "Mumbai"}}}
}
```

**Step 4: Server Execution**
```
Server calls wttr.in API → Gets weather data → Returns JSON response
```

**Step 5: Response Generation**
```
LLM receives raw data → Generates natural response
Output: "The weather in Mumbai is currently 28°C with partly cloudy skies. 
         The humidity is at 70% with winds at 15 km/h."
```

---

## 🧪 Testing

The system includes 4 test cases:

```python
tests = [
    "What's the weather in Mumbai?",      # Uses get_weather
    "Tell me about the weather in Delhi", # Uses get_weather
    "Search for latest news about AI",    # Uses web_search
    "What is Model Context Protocol?"     # Uses web_search
]
```

### Expected Output
```
USER: What's the weather in Mumbai?
🤖 Routing decision: User is asking for weather information
AGENT: The current weather in Mumbai is 28°C (82°F) with partly cloudy 
       conditions. Humidity is at 70% with winds at 15 km/h.
```

---

## 🔧 Key Technologies

| Technology | Purpose |
|------------|---------|
| **FastMCP** | Framework for building MCP servers quickly |
| **LangGraph** | Build stateful, multi-step LLM applications |
| **OpenAI GPT-4** | Intelligent routing and natural language generation |
| **JSON-RPC** | Protocol for client-server communication |
| **Pydantic** | Data validation and schema definition |
| **STDIO** | Communication channel between client and server |

---

## 🌟 Why MCP Matters

### Traditional Approach (Without MCP)
- Each tool needs custom integration
- No standardization
- Difficult to maintain and scale
- Tool discovery is manual

### With MCP
- ✅ Standardized protocol
- ✅ Automatic tool discovery
- ✅ Easy to add new tools
- ✅ Interoperable across different AI systems
- ✅ Clear separation of concerns

---

## 🔒 Security Considerations

1. **API Keys**: Store in `.env` file, never commit to version control
2. **Input Validation**: Pydantic models validate all inputs
3. **Error Handling**: Graceful error handling for API failures
4. **Timeouts**: API calls have timeouts to prevent hanging

---

## 🚧 Extending the System

### Adding a New Tool

1. **Define the tool in `mcp_server.py`:**
```python
class CalculatorInput(BaseModel):
    expression: str

@mcp.tool()
def calculate(input: CalculatorInput):
    """Evaluate mathematical expressions"""
    try:
        result = eval(input.expression)  # Use safe_eval in production
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
```

2. **Update routing logic in `mcp_client.py`:**
```python
# Add to available tools in routing_prompt
# The LLM will automatically learn to use it
```

3. **Test it:**
```python
"What is 25 * 4 + 10?"  # Should use calculator tool
```

---

## 📊 LangGraph Visualization

The system generates a visual representation of the agent workflow:

```
┌─────────┐
│  START  │
└────┬────┘
     │
     ▼
┌─────────┐
│  Route  │  ← Determines which tool to use
└────┬────┘
     │
     ▼
┌──────────┐
│ Respond  │  ← Generates natural language response
└────┬─────┘
     │
     ▼
┌─────────┐
│   END   │
└─────────┘
```

Saved as `langgraph_diagram.png`

---

## 🐛 Troubleshooting

### Issue: "SERPER_API_KEY not configured"
**Solution**: Add your Serper API key to `.env` file

### Issue: Weather API timeout
**Solution**: Check internet connection; wttr.in might be temporarily unavailable

### Issue: OpenAI API errors
**Solution**: Verify `OPEN_AI_KEY` in `.env` and check API quota

### Issue: Graph visualization fails
**Solution**: Install graphviz: `brew install graphviz` (macOS)

---

## 📚 Resources

- **MCP Specification**: https://spec.modelcontextprotocol.io/
- **FastMCP Documentation**: https://github.com/jlowin/fastmcp
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **OpenAI API**: https://platform.openai.com/docs

---

## 📄 License

This project is for educational purposes. Please ensure you comply with the terms of service for all external APIs used.

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add more tools (database queries, file operations, etc.)
- Implement HTTP transport (in addition to STDIO)
- Add authentication and authorization
- Implement tool composition (chaining multiple tools)
- Add conversation memory and context

---

## 📧 Contact

For questions or feedback, please open an issue in the repository.

---

**Made with ❤️ using MCP, LangGraph, and OpenAI**
