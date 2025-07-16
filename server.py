from mcp.server.fastmcp import FastMCP
from pymongo import MongoClient
from bson.json_util import dumps
from typing import Literal, Dict, Any, Optional
import argparse
import uvicorn

# Initialize MCP server
mcp = FastMCP(
    name="Simple MongoDB MCP Server",
    description="A server that interacts with a MongoDB database using MCP",
    host="0.0.0.0",   
    port=3333         # Custom port
)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["MCP_Sample"]

# Define a tool for interacting with MongoDB
@mcp.tool()
def mongo_action(
    action: Literal["list_collections", "find", "insert"],
    collection: Optional[str] = None,
    query: Optional[Dict[str, Any]] = None,
    document: Optional[Dict[str, Any]] = None
) -> Any:
    """Perform a MongoDB action like listing collections, finding documents, or inserting a document."""

    if action == "list_collections":
        return {"collections": db.list_collection_names()}

    elif action == "find":
        if not collection:
            return {"error": "Missing 'collection'"}
        results = list(db[collection].find(query or {}))
        return dumps(results)

    elif action == "insert":
        if not collection or not document:
            return {"error": "Missing 'collection' or 'document'"}
        result = db[collection].insert_one(document)
        return {"inserted_id": str(result.inserted_id)}

    else:
        return {"error": "Unknown or unsupported action"}
    

# if __name__ == "__main__":
#     print("MCP server is running on http://0.0.0.0:3333 (IP 10.1.7.110)")
#     # mcp.run()
#     mcp.run(transport="streamable-http")
#     # mcp.run(mcp.streamable_http_app,host="localhost", port=3333)


if __name__ == "__main__":
    print("MCP server is running on http://0.0.0.0:3333 (IP 10.1.7.110)")
    parser = argparse.ArgumentParser(description="Run MCP Streamable HTTP based server")
    parser.add_argument("--port", type=int, default=3333, help="Localhost port to listen on")
    args = parser.parse_args()

    uvicorn.run(mcp.streamable_http_app, host="0.0.0.0", port=args.port)
