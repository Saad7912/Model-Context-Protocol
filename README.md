# 🧠 MCP-Based LLM Agent with Tool Use

This project demonstrates a **Model Context Protocol (MCP)**-enabled conversational agent powered by **LangChain** and **Groq's LLMs**, with support for external tools like **DuckDuckGo search**, **weather**, and **MongoDB** access.

## 🚀 Features

- **Interactive Chat Interface** with memory support
- **Dynamic tool usage** via MCP (web search, weather, MongoDB)
- **Runs external tools** using MCP servers defined in `browser_mcp.json`
- Powered by **Groq's Qwen-QWQ-32B model** using LangChain


## 🧩 What is Model Context Protocol (MCP)?

**Model Context Protocol (MCP)** is a lightweight interface for connecting LLMs with external tools (like APIs or databases). The **MCP Server** handles tool execution and sends results back to the LLM agent, enabling it to reason and respond based on real-world data.

## 🛠️ Tools Used (via MCP Servers)

- **DuckDuckGo Search**
- **Weather API Tool** (`@h1deya/mcp-server-weather`)
- **MongoDB Tool** (via both `mongodb-mcp-server` and local `mongo_tools.py`)

Defined inside `browser_mcp.json` using:

```json
{
  "mcpServers": {
    "duckduckgo-search": {
      "command": "npx",
      "args": ["-y", "duckduckgo-mcp-server"]
    },
    "weather": {
      "command": "npx",
      "args": ["-y", "@h1deya/mcp-server-weather"]
    },
    "MongoDB": {
      "command": "npx",
      "args": ["-y", "mongodb-mcp-server", "--connectionString", "mongodb://localhost:27017/MCP_Sample"]
    },
    "mongo": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "C:\\Users\\G3NZ\\Summer2025\\MCP_DataBase\\mcp_tools\\mongo_tools.py"
      ]
    }
  }
}
```
## ⚙️ How to Run
### Clone this repository
```
https://github.com/Saad7912/Model-Context-Protocol.git
```

