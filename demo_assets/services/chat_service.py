"""
Chat service for handling AI chat functionality using OpenRouter API
"""
import os
import json
import aiohttp
import markdown
import logging
from typing import Dict, Any, AsyncGenerator
from fastapi import HTTPException
from dependencies.config import get_settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LLM Configuration - Uses environment variable with fallback
LLM_MODEL = os.getenv("OPENROUTER_LLM_MODEL", "meta-llama/llama-3.3-70b-instruct:free")

# Print LLM model being used to console
print(f"🤖 Using LLM Model: {LLM_MODEL}")
logger.info(f"LLM Model configured: {LLM_MODEL}")

# Alternative models you can use (set OPENROUTER_LLM_MODEL in your .env file):
# OPENROUTER_LLM_MODEL=meta-llama/llama-3.3-70b-instruct  # Paid version
# OPENROUTER_LLM_MODEL=qwen/qwen3-coder:free              # Qwen3 Coder


class ChatService:
    """Service for AI chat operations using OpenRouter API"""

    @staticmethod
    async def test_connection() -> Dict[str, Any]:
        """
        Test method to check if the OpenRouter API is accessible

        Returns:
            dict: Connection test result
        """
        try:
            settings = get_settings()
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                return {"status": "error", "message": "No API key found", "api_key_length": 0}

            if settings.debug:
                print(f"DEBUG: Testing connection with API key: {api_key[:10]}...")

            # Simple test payload
            test_payload = {
                "model": LLM_MODEL,
                "messages": [
                    {"role": "user", "content": "Hello"}
                ],
                "max_tokens": 10
            }

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://localhost",
                "X-Title": "FastOpp AI Demo"
            }

            if settings.debug:
                print("DEBUG: Making test request to OpenRouter...")

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=test_payload
                ) as response:
                    if settings.debug:
                        print(f"DEBUG: Test response status: {response.status}")

                    if response.status == 200:
                        result = await response.json()
                        if settings.debug:
                            print(f"DEBUG: Test response: {result}")
                        return {
                            "status": "success",
                            "message": "API connection successful",
                            "response": result
                        }
                    else:
                        error_text = await response.text()
                        if settings.debug:
                            print(f"DEBUG: Test error: {error_text}")
                        
                        # Provide more specific error messages
                        if response.status == 401:
                            return {
                                "status": "error",
                                "message": "Authentication failed. Please check your OPENROUTER_API_KEY is correct and valid.",
                                "status_code": response.status
                            }
                        elif response.status == 400:
                            if "model" in error_text.lower() and ("not found" in error_text.lower() or "unavailable" in error_text.lower()):
                                return {
                                    "status": "error",
                                    "message": f"The LLM model '{LLM_MODEL}' is not available. Please try a different model or check OpenRouter's available models.",
                                    "status_code": response.status
                                }
                            else:
                                return {
                                    "status": "error",
                                    "message": f"Bad request: {error_text}",
                                    "status_code": response.status
                                }
                        elif response.status == 429:
                            return {
                                "status": "error",
                                "message": "Rate limit exceeded. Please try again later.",
                                "status_code": response.status
                            }
                        else:
                            return {
                                "status": "error",
                                "message": f"API error (status {response.status}): {error_text}",
                                "status_code": response.status
                            }

        except Exception as e:
            if settings.debug:
                print(f"DEBUG: Test exception: {e}")
            return {"status": "error", "message": f"Exception: {str(e)}"}

    @staticmethod
    async def chat_with_llama(user_message: str) -> Dict[str, Any]:
        """
        Send a message to Llama 3.3 70B via OpenRouter API (non-streaming)
        
        Args:
            user_message: The user's message to send to the AI
            
        Returns:
            dict: Response containing the AI's reply and model info
            
        Raises:
            HTTPException: If there's an error with the API call
        """
        try:
            settings = get_settings()
            if not user_message:
                raise HTTPException(status_code=400, detail="Message is required")
            
            # Get API key from environment
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise HTTPException(status_code=500, detail="OpenRouter API key not configured")
            
            logger.info(f"Starting chat request with message: {user_message[:50]}...")
            logger.info(f"API key found: {api_key[:10]}...")
            if settings.debug:
                print(f"DEBUG: Starting chat request with message: {user_message[:50]}...")
                print(f"DEBUG: API key found: {api_key[:10]}...")
            
            # Prepare the request to OpenRouter
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://localhost",  # More generic referer
                "X-Title": "FastOpp AI Demo"
            }
            
            # free model is meta-llama/llama-3.3-70b-instruct:free
            # paid model is meta-llama/llama-3.3-70b-instruct
            # https://openrouter.ai/meta-llama/llama-3.3-70b-instruct:free/api
            payload = {
                "model": LLM_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful AI assistant. Provide clear, concise, "
                            "and accurate responses. Be friendly and engaging in your "
                            "communication style. IMPORTANT: Always format your responses "
                            "using markdown syntax for better readability. Use **bold** for emphasis, "
                            "*italic* for subtle emphasis, `code` for inline code, ```code blocks``` "
                            "for multi-line code, and proper markdown formatting for lists, "
                            "headings, and other structured content."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            logger.info(f"Making request to OpenRouter with payload: {json.dumps(payload, indent=2)}")
            if settings.debug:
                print(f"DEBUG: Making request to OpenRouter with payload: {json.dumps(payload, indent=2)}")
            
            # Make request to OpenRouter
            async with aiohttp.ClientSession() as session:
                if settings.debug:
                    print("DEBUG: Created aiohttp session")
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if settings.debug:
                        print(f"DEBUG: Got response from OpenRouter, status: {response.status}")
                    logger.info(f"OpenRouter response status: {response.status}")
                    logger.info(f"OpenRouter response headers: {dict(response.headers)}")
                    
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"OpenRouter API error: {error_text}")
                        
                        # Provide more specific error messages
                        if response.status == 401:
                            raise HTTPException(
                                status_code=401, 
                                detail="Authentication failed. Please check your OPENROUTER_API_KEY is correct and valid."
                            )
                        elif response.status == 400:
                            # Check if it's a model availability issue
                            if "model" in error_text.lower() and ("not found" in error_text.lower() or "unavailable" in error_text.lower()):
                                raise HTTPException(
                                    status_code=400,
                                    detail=f"The LLM model '{LLM_MODEL}' is not available. Please try a different model or check OpenRouter's available models."
                                )
                            else:
                                raise HTTPException(
                                    status_code=400,
                                    detail=f"Bad request: {error_text}"
                                )
                        elif response.status == 429:
                            raise HTTPException(
                                status_code=429,
                                detail="Rate limit exceeded. Please try again later."
                            )
                        else:
                            raise HTTPException(
                                status_code=500, 
                                detail=f"OpenRouter API error (status {response.status}): {error_text}"
                            )
                    
                    result = await response.json()
                    logger.info(f"OpenRouter response: {json.dumps(result, indent=2)}")
                    if settings.debug:
                        print(f"DEBUG: OpenRouter response: {json.dumps(result, indent=2)}")
                    
                    # Extract the assistant's response
                    assistant_message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
                    if not assistant_message:
                        logger.warning("No assistant message content found in response")
                        logger.warning(f"Full response structure: {result}")
                        if settings.debug:
                            print("DEBUG: No assistant message content found in response")
                            print(f"DEBUG: Full response structure: {result}")
                    
                    # Convert markdown to HTML
                    formatted_html = markdown.markdown(
                        assistant_message,
                        extensions=['fenced_code', 'codehilite', 'tables', 'nl2br']
                    )
                    
                    logger.info(f"Successfully processed response, length: {len(assistant_message)}")
                    if settings.debug:
                        print(f"DEBUG: Successfully processed response, length: {len(assistant_message)}")
                    
                    return {
                        "response": formatted_html,
                        "raw_response": assistant_message,  # Keep original for debugging
                        "model": LLM_MODEL
                    }
                    
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            if settings.debug:
                print(f"DEBUG: JSON decode error: {e}")
            raise HTTPException(status_code=400, detail="Invalid JSON")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            if settings.debug:
                print(f"DEBUG: Unexpected error: {e}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    @staticmethod
    async def chat_with_llama_stream(user_message: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream a message to Llama 3.3 70B via OpenRouter API with server-side markdown processing
        
        Args:
            user_message: The user's message to send to the AI
            
        Yields:
            dict: Streaming response chunks from the AI with HTML formatting
            
        Raises:
            HTTPException: If there's an error with the API call
        """
        try:
            if not user_message:
                raise HTTPException(status_code=400, detail="Message is required")
            
            # Get API key from environment
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise HTTPException(status_code=500, detail="OpenRouter API key not configured")
            
            logger.info(f"Starting streaming chat request with message: {user_message[:50]}...")
            logger.info(f"API key found: {api_key[:10]}...")
            
            # Prepare the request to OpenRouter
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://localhost",  # More generic referer
                "X-Title": "FastOpp AI Demo"
            }
            # free model is meta-llama/llama-3.3-70b-instruct:free
            # https://openrouter.ai/meta-llama/llama-3.3-70b-instruct:free/api
            # paid model is meta-llama/llama-3.3-70b-instruct
            payload = {
                "model": LLM_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful AI assistant. Provide clear, concise, "
                            "and accurate responses. Be friendly and engaging in your "
                            "communication style. IMPORTANT: Always format your responses "
                            "using markdown syntax for better readability. Use **bold** for emphasis, "
                            "*italic* for subtle emphasis, `code` for inline code, ```code blocks``` "
                            "for multi-line code, and proper markdown formatting for lists, "
                            "headings, and other structured content."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000,
                "stream": True  # Enable streaming
            }
            
            logger.info(f"Making streaming request to OpenRouter with payload: {json.dumps(payload, indent=2)}")
            
            # Make streaming request to OpenRouter
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    logger.info(f"OpenRouter streaming response status: {response.status}")
                    logger.info(f"OpenRouter streaming response headers: {dict(response.headers)}")
                    
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"OpenRouter API streaming error: {error_text}")
                        raise HTTPException(status_code=500, detail=f"OpenRouter API error: {error_text}")
                    
                    # Accumulate raw content for markdown processing
                    accumulated_content = ""
                    chunk_count = 0
                    
                    logger.info("Starting to stream response...")
                    
                    # Stream the response
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        if line.startswith('data: '):
                            data = line[6:]  # Remove 'data: ' prefix
                            if data == '[DONE]':
                                logger.info("Stream completed with [DONE]")
                                break
                            
                            try:
                                chunk = json.loads(data)
                                chunk_count += 1
                                logger.debug(f"Received chunk {chunk_count}: {chunk}")
                                
                                if 'choices' in chunk and len(chunk['choices']) > 0:
                                    delta = chunk['choices'][0].get('delta', {})
                                    content = delta.get('content', '')
                                    if content:
                                        # Accumulate the raw content
                                        accumulated_content += content
                                        
                                        # Convert accumulated content to HTML
                                        formatted_html = markdown.markdown(
                                            accumulated_content,
                                            extensions=['fenced_code', 'codehilite', 'tables', 'nl2br']
                                        )
                                        # free model is meta-llama/llama-3.3-70b-instruct:free
                                        # https://openrouter.ai/meta-llama/llama-3.3-70b-instruct:free/api
                                        # paid model is meta-llama/llama-3.3-70b-instruct
                                        yield {
                                            "content": formatted_html,
                                            "raw_content": accumulated_content,
                                            "model": LLM_MODEL
                                        }
                            except json.JSONDecodeError as e:
                                logger.warning(f"JSON decode error in chunk: {e}, chunk: {data}")
                                continue  # Skip invalid JSON chunks
                    
                    logger.info(
                        f"Streaming completed. Total chunks: {chunk_count}, "
                        f"Final content length: {len(accumulated_content)}"
                    )
                    
        except Exception as e:
            logger.error(f"Unexpected error in streaming: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    @staticmethod
    async def _mock_stream_response(user_message: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Mock streaming response for testing when API is not available
        
        Args:
            user_message: The user's message
            
        Yields:
            dict: Mock streaming response chunks with HTML formatting
        """
        import asyncio
        
        # Mock response based on user message
        if "story" in user_message.lower():
            response_parts = [
                "Once upon a time, in a **distant galaxy**, there lived a curious robot named ",
                "**Rusty**. Unlike other robots who spent their days processing data, Rusty had a ",
                "dream: to understand the meaning of *human emotions*. \n\n",
                "Every day, Rusty would observe the humans from afar, watching them laugh, cry, ",
                "and share moments of joy. The robot's circuits would buzz with questions: ",
                "`What makes them smile?` `Why do they hold hands?` `What is love?`\n\n",
                "One day, Rusty decided to take a bold step. Instead of staying in the shadows, ",
                "the robot approached a group of children playing in the park. At first, the ",
                "children were surprised, but Rusty's gentle nature and endless curiosity ",
                "soon won them over.\n\n",
                "Through their friendship, Rusty learned that emotions weren't just data to be ",
                "processed—they were experiences to be felt. The robot discovered that ",
                "**empathy** was the bridge between artificial and human intelligence.\n\n",
                "And so, Rusty became the first robot to truly understand the heart, proving ",
                "that sometimes the most profound discoveries come from the simplest connections."
            ]
        else:
            response_parts = [
                "Hello! I'm **Midori**, your AI assistant. I'm here to help you with ",
                "any questions or tasks you might have. I can assist with:\n\n",
                "- **Writing and editing** content\n",
                "- **Problem solving** and analysis\n",
                "- **Creative projects** and brainstorming\n",
                "- **Learning** new topics\n",
                "- **Coding** and technical questions\n\n",
                "What would you like to explore today? I'm excited to help you discover ",
                "new possibilities and find solutions to your challenges!"
            ]
        
        # Accumulate content for markdown processing
        accumulated_content = ""
        
        # Stream the response with delays to simulate real streaming
        for part in response_parts:
            await asyncio.sleep(0.1)  # Small delay between chunks
            accumulated_content += part
            
            # Convert accumulated content to HTML
            formatted_html = markdown.markdown(
                accumulated_content,
                extensions=['fenced_code', 'codehilite', 'tables', 'nl2br']
            )
            
            yield {
                "content": formatted_html,
                "raw_content": accumulated_content,
                "model": LLM_MODEL
            } 