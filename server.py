# from fastapi import FastAPI
# from pydantic import BaseModel
# import asyncio
# from mcp_use import MCPAgent, MCPClient
# from langchain_groq import ChatGroq
# import os
# from dotenv import load_dotenv

# # Load .env and API key
# load_dotenv()
# groq_key = os.getenv("GROQ_API_KEY")

# # FastAPI app
# app = FastAPI()

# # Request model
# class QuestionRequest(BaseModel):
#     question: str

# # Shared variables (load once)
# config_file = "browser_mcp.json"
# client = MCPClient.from_config_file(config_file)
# llm = ChatGroq(model="qwen-qwq-32b", groq_api_key=groq_key)
# agent = MCPAgent(llm=llm, client=client, max_steps=15, memory_enabled=True)

# # POST endpoint
# @app.post("/chat")
# async def chat_endpoint(req: QuestionRequest):
#     response = await agent.run(req.question)
#     return {"response": response}



#----------------------------------------------------------------
from fastapi import FastAPI, Request
from fastapi_mcp import FastApiMCP
from pymongo import MongoClient
from bson.json_util import dumps
from fastapi.responses import JSONResponse

app = FastAPI()
mcp = FastApiMCP(app,
                 name="Simple FastAPI MCP" ,
                 description="A simple FastAPI MCP server")
mcp.mount()

client = MongoClient("mongodb://localhost:27017/")
db = client["MCP_Sample"]  

@app.post("/query")
async def handle_query(request: Request):
    payload = await request.json()

    if payload.get("action") == "list_collections":
        return {"collections": db.list_collection_names()}

    elif payload.get("action") == "find":
        collection_name = payload.get("collection")
        query = payload.get("query", {})
        if not collection_name:
            return {"error": "Missing 'collection'"}
        results = list(db[collection_name].find(query))
        return JSONResponse(content=dumps(results))

    elif payload.get("action") == "insert":
        collection_name = payload.get("collection")
        document = payload.get("document")
        if not collection_name or not document:
            return {"error": "Missing 'collection' or 'document'"}
        result = db[collection_name].insert_one(document)
        return {"inserted_id": str(result.inserted_id)}

    else:
        return {"error": "Unknown or missing action"}

mcp.setup_server()