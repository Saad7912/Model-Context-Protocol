# 🧠 MCP-Based LLM Agent and FastAPI MongoDB Server

This project combines a **Model Context Protocol (MCP)**-enabled conversational agent powered by LangChain and Groq's LLMs with a **FastAPI MongoDB server** for managing collections. The agent uses MCP servers for tools (web search, weather, MongoDB), while the FastAPI server provides REST endpoints for MongoDB operations.


## Features
### LLM Agent
- Interactive chat interface with memory support.
- Dynamic tool usage via MCP (DuckDuckGo search, Weather API, MongoDB).
- Powered by Groq’s Qwen-QWQ-32B model using LangChain.
- Configured via browser_mcp.json for MCP servers.

### FastAPI MongoDB Server
- /find: Search documents using any field (e.g., name, source_code).
- /insert: Add documents with any fields to a collection.
- /schema: Get field names and data types of a collection.
- Supports MongoDB’s schemaless nature for flexible queries and inserts.
- Works with MCP Inspector UI and curl.

  ## Prerequisites
  - **Python 3.9+:** Install from python.org.
  - **MongoDB:** Install locally or use MongoDB Atlas (mongodb://localhost:27017).
  - **Node.js:** For MCP servers like duckduckgo-mcp-server and @h1deya/mcp-server-weather.
  - **Python packages:**
    - **Agent:** langchain, langchain-groq, mcp[cli].
    - **FastAPI:** fastapi, pymongo, pydantic, uvicorn, fastapi_mcp.
  - **MCP Inspector:** For UI testing, accessible via VS Code Simple Browser or Chrome.
  - **Groq API Key:** Required for the LLM agent.
 
  ## Installation
1. **Clone the repository:**
  ```
  git clone https://github.com/Saad7912/Model-Context-Protocol.git
  cd Model-Context-Protocol
 ```
2. **Set up a virtual environment (recommended):**

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. **Install dependencies:**
```
langchain
langchain-groq
mcp[cli]
fastapi
pymongo
pydantic
uvicorn
fastapi_mcp
```
4. **Configure MongoDB:**
```
- Ensure MongoDB is running on mongodb://localhost:27017.
- Create a database with collections.
```
5. **Set Groq API Key** (for LLM agent):
```
GROQ_API_KEY=your-groq-api-key-here
```

## **Running the Project**
1. **LLM Agent:**
   
   i. Start MCP servers (defined in browser_mcp.json):      
   ```
   npx -y duckduckgo-mcp-server
   npx -y @h1deya/mcp-server-weather
   npx -y mongodb-mcp-server --connectionString mongodb://localhost:27017/MCP_Sample
   uv run --with mcp[cli] mcp run ./agent/mongo_tools.py
   ```
  
   ii. **Run the agent:**
   ```
   uv run app.py
   ```

   iii. **Interact via the chat interface or MCP Inspector.**


2. **FastAPI MongoDB Server:**
   
   i. **Start the server:**
      ```
      uvicorn api.main:app --host 0.0.0.0 --port 4444
      ```
   ii. **Open MCP Inspecto:**
      - Set URL to http://localhost:4444/mcp, transport to SSE.

## Endpoints (FastAPI)
**/find (Find Documents)**
 - **Method:** POST
 - **Input:**
   - collection: String (e.g., layout_1000).
   - query_json: JSON string (e.g., {"name": "DummyData"}).
- Output: {"results": [...]} (list of matching documents).
- **Example:**
  ```
  curl -X POST http://localhost:4444/find -H "Content-Type: application/json" -d '{"collection": "layout_1000", "query": {"name": "DummyData"}}'

- **Inspector:** Set collection: "layout_1000", query_json: {"name": "DummyData"}.

**/insert (Insert Document)**
- **Method:** POST
- **Input:**
  - collection: String (e.g., layout_1000).
  - document_json: JSON string (e.g., {"name": "TestData", "address": "0x123"}).
- **Output:** {"inserted_id": "<id>"}.
- **Example:**
  ```
  curl -X POST http://localhost:4444/insert -H "Content-Type: application/json" -d '{"collection": "layout_1000", "document": {"name": "TestData", "address": "0x123"}}'
- Inspector: Set collection: "layout_1000", document_json: {"name": "TestData"}.

**/schema (Get Collection Schema)**
- **Method:** POST
- **Input:**
  - collection: String (e.g., layout_1000).
- **Output:** {"fields": [{"name": "name", "types": ["str"]}, ...]}.
- **Example:**
  ```
  curl -X POST http://localhost:4444/schema -H "Content-Type: application/json" -d '{"collection": "layout_1000"}'
- Inspector: Set collection: "layout_1000".
  
## Testing
- **MCP Inspector** (FastAPI):
  - Open http://127.0.0.1:6274 in Chrome.
  - Select endpoint (e.g., find_documents_find_post).
  - Enter inputs (e.g., query_json: {"source_code": "code"}).
- **MongoDB Compass:**
   - Connect to mongodb://localhost:27017/MCP_Sample.
   - Verify documents or schemas.
- **Logs:**
  - Check terminal for DEBUG, WARNING, or ERROR messages.

## Contributing
Submit issues or pull requests to improve the agent or API!

## License
MIT License
