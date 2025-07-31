from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Any
from bson import ObjectId
from datetime import datetime
import logging
from fastapi_mcp import FastApiMCP
from pymongo import MongoClient
import json  
from collections import defaultdict


app = FastAPI()
mcp = FastApiMCP(app,
                 name="Simple FastAPI MCP",
                 description="A simple FastAPI MCP server with separate endpoints")
mcp.mount()


client = MongoClient("mongodb://localhost:27017/")
db = client["MCP_Sample"]

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


#FindResponse End point pydantic Model
class FindResponse(BaseModel):
    results: List[Dict[str, Any]]

def convert_mongo_document(doc):
    if not isinstance(doc, dict):
        logger.error(f"Document is not a dict: {type(doc)}")
        return {}
    result = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            result[key] = str(value)
        elif isinstance(value, datetime):
            result[key] = value.isoformat()
        elif isinstance(value, (list, tuple)):
            result[key] = [convert_mongo_document(v) if isinstance(v, dict) else v for v in value]
        elif isinstance(value, dict):
            result[key] = convert_mongo_document(value)
        else:
            result[key] = value
    return result


#Insert Endpoint pydantic model
class InsertResponse(BaseModel):
    inserted_id: str

#SchemaResponse Endpoint pydantic model
class FieldInfo(BaseModel):
    name: str
    types: List[str]

class SchemaResponse(BaseModel):
    fields: List[FieldInfo]

def get_field_info(doc, field_types):
    if isinstance(doc, dict):
        for key, value in doc.items():
            if key != '_id':  # Skip MongoDB's internal _id
                field_types[key].add(type(value).__name__)
        for key, value in doc.items():
            if isinstance(value, dict):
                get_field_info(value, field_types)

#Endpoint 1
@app.post("/list_collections")
async def list_collections():
    return {"collections": db.list_collection_names()}



#Endpoint 2
@app.post("/schema", response_model=SchemaResponse)
async def get_collection_schema(
    request: Request,
    collection: str = "layout_1000"
):
    try:
        raw_body = await request.body()
        logger.debug(f"Raw request body: {raw_body!r}")
        headers = dict(request.headers)
        logger.debug(f"Request headers: {headers}")

        payload = {}
        if raw_body:
            try:
                payload = await request.json()
                if isinstance(payload, dict) and "params" in payload:
                    payload = payload.get("params", {})
            except ValueError as json_err:
                logger.warning(f"Invalid JSON payload: {str(json_err)}")
                return JSONResponse(status_code=400, content={"error": "Invalid JSON payload"})

        collection_name = payload.get("collection", collection)

        if collection_name not in db.list_collection_names():
            logger.debug(f"Collection '{collection_name}' does not exist")
            return JSONResponse(status_code=404, content={"error": f"Collection '{collection_name}' not found"})

        # Sample up to 100 documents
        sample_size = 100
        total_docs = min(db[collection_name].count_documents({}), sample_size)
        if total_docs == 0:
            logger.debug(f"Collection '{collection_name}' is empty")
            return {"fields": []}

        field_types = defaultdict(set)

        for doc in db[collection_name].find().limit(sample_size):
            get_field_info(doc, field_types)

        fields = [
            {
                "name": field,
                "types": sorted(list(field_types[field]))
            }
            for field in sorted(field_types.keys())
        ]

        logger.debug(f"Schema fields for '{collection_name}': {fields}")
        return {"fields": fields}
    except Exception as e:
        logger.error(f"Error in get_collection_schema: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})

#Endpoint 3
@app.post("/find", response_model=FindResponse)
async def find_documents(
    request: Request,
    collection: str = "layout_1000",
    query_json: str | None = None
):
    try:
        raw_body = await request.body()
        logger.debug(f"Raw request body: {raw_body!r}")
        headers = dict(request.headers)
        logger.debug(f"Request headers: {headers}")

        payload = {}
        if raw_body:
            try:
                payload = await request.json()
                if isinstance(payload, dict) and "params" in payload:
                    payload = payload.get("params", {})
            except ValueError as json_err:
                logger.warning(f"Invalid JSON payload: {str(json_err)}")
                return JSONResponse(status_code=400, content={"error": "Invalid JSON payload"})

        collection_name = payload.get("collection", collection)
        query = None
        if "query" in payload:
            query = payload.get("query")
        elif query_json:
            try:
                query = json.loads(query_json)
                if not isinstance(query, dict):
                    logger.warning("query_json must be a JSON object")
                    return JSONResponse(status_code=400, content={"error": "query_json must be a JSON object"})
            except json.JSONDecodeError:
                logger.warning("Invalid JSON in query_json")
                return JSONResponse(status_code=400, content={"error": "Invalid JSON in query_json"})

        if not query:
            logger.warning("Query is missing")
            return JSONResponse(status_code=400, content={"error": "Query is required"})

        if collection_name not in db.list_collection_names():
            logger.debug(f"Collection '{collection_name}' does not exist")
            return JSONResponse(status_code=404, content={"error": f"Collection '{collection_name}' not found"})

        results = [convert_mongo_document(doc) for doc in db[collection_name].find(query)]
        logger.debug(f"Query results: {results}")
        return {"results": results}
    except Exception as e:
        logger.error(f"Error in find_documents: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})



#Endpoint 4
@app.post("/insert", response_model=InsertResponse)
async def insert_document(
    request: Request,
    collection: str = "layout_1000",
    document_json: str | None = None
):
    try:
        raw_body = await request.body()
        logger.debug(f"Raw request body: {raw_body!r}")
        headers = dict(request.headers)
        logger.debug(f"Request headers: {headers}")

        payload = {}
        if raw_body:
            try:
                payload = await request.json()
                if isinstance(payload, dict) and "params" in payload:
                    payload = payload.get("params", {})
            except ValueError as json_err:
                logger.warning(f"Invalid JSON payload: {str(json_err)}")
                return JSONResponse(status_code=400, content={"error": "Invalid JSON payload"})

        collection_name = payload.get("collection", collection)
        document = None
        if "document" in payload:
            document = payload.get("document")
        elif document_json:
            try:
                document = json.loads(document_json)
                if not isinstance(document, dict):
                    logger.warning("document_json must be a JSON object")
                    return JSONResponse(status_code=400, content={"error": "document_json must be a JSON object"})
            except json.JSONDecodeError:
                logger.warning("Invalid JSON in document_json")
                return JSONResponse(status_code=400, content={"error": "Invalid JSON in document_json"})

        if not document:
            logger.warning("Document is missing")
            return JSONResponse(status_code=400, content={"error": "Document is required"})

        if collection_name not in db.list_collection_names():
            logger.debug(f"Creating collection '{collection_name}'")
            db.create_collection(collection_name)

        result = db[collection_name].insert_one(document)
        logger.debug(f"Inserted document with ID: {result.inserted_id}")
        return {"inserted_id": str(result.inserted_id)}
    except Exception as e:
        logger.error(f"Error in insert_document: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})
    



mcp.setup_server()
