"""
Chat routes for AI chat functionality
"""
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from services.chat_service import ChatService
import json

router = APIRouter()


@router.get("/chat/test")
async def test_chat_connection():
    """Test endpoint to check OpenRouter API connection"""
    try:
        result = await ChatService.test_connection()
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Test failed: {str(e)}"}
        )


@router.post("/chat")
async def chat_with_llama(request: Request):
    """Chat endpoint using OpenRouter API with Llama 3.3 70B (non-streaming)"""
    try:
        # Get the request body
        body = await request.json()
        user_message = body.get("message", "")
        
        if not user_message:
            return JSONResponse(
                status_code=400,
                content={"error": "Message is required"}
            )
        
        # Use service to handle chat
        response = await ChatService.chat_with_llama(user_message)
        return JSONResponse(content=response)
        
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )


@router.post("/chat/stream")
async def chat_with_llama_stream(request: Request):
    """Streaming chat endpoint using OpenRouter API with Llama 3.3 70B"""
    try:
        # Get the request body
        body = await request.json()
        user_message = body.get("message", "")
        
        if not user_message:
            return JSONResponse(
                status_code=400,
                content={"error": "Message is required"}
            )
        
        # Create SSE response
        async def event_generator():
            try:
                async for chunk in ChatService.chat_with_llama_stream(user_message):
                    yield {
                        "event": "message",
                        "data": json.dumps(chunk)
                    }
                # Send completion event
                yield {
                    "event": "complete",
                    "data": json.dumps({"status": "completed"})
                }
            except Exception as e:
                yield {
                    "event": "error",
                    "data": json.dumps({"error": str(e)})
                }
        
        return EventSourceResponse(event_generator())
        
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        ) 