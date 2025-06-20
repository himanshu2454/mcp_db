import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Services.ToolService import get_tool_service, ToolService
from Services.LLMs.Groq.GroqSerivce import get_groq_service, GroqService
from Services.LoggerService import get_logger
from bson import ObjectId
from datetime import datetime

logger = get_logger("MCP.Main")

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_sessions = set()

# Define request model
class ChatRequest(BaseModel):
    sessionId: str
    message: str

def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, list):
        return [convert_objectid(item) for item in obj]
    if isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    return obj

@app.post("/api/chat")
async def chat_endpoint(
    request: ChatRequest,
    tool_service: ToolService = Depends(get_tool_service),
    groq_service: GroqService = Depends(get_groq_service)
):
    try:
        logger.info("Received chat request: sessionId=%s, message=%s", request.sessionId, request.message)
        if not request.sessionId or len(request.sessionId) > 100:
            raise HTTPException(status_code=400, detail="Invalid sessionId")
        if not request.message or len(request.message) > 1000:
            raise HTTPException(status_code=400, detail="Message too long or empty")

        response = await groq_service.query([{"role": "user", "content": request.message}])
        logger.info("Groq response: %s", response)

        is_db_related = response.get("isDbRelated", False)
        result = response.get("response", "No response provided")

        if is_db_related:
            try:
                if isinstance(result, str):
                    result = json.loads(result)
                db_result = tool_service.db_call(result, user_prompt=request.message)
                logger.info("Database query result: %s", db_result)
                # Convert ObjectId to string for JSON serialization
                db_result = convert_objectid(db_result)
                return JSONResponse({"reply": db_result})
            except Exception as e:
                logger.error("Error executing database query: %s", e)
                return JSONResponse({"reply": f"Error executing database query: {str(e)}"}, status_code=500)
        else:
            logger.info("Non-database response: %s", result)
            return JSONResponse({"reply": result})
    except HTTPException as he:
        logger.error("HTTP error: %s", he)
        raise he
    except Exception as e:
        logger.error("Unexpected error in chat endpoint: %s", e)
        return JSONResponse({"reply": f"Unexpected error: {str(e)}"}, status_code=500)