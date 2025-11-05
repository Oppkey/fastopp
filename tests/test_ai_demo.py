#!/usr/bin/env python3
"""
Simple test script for the AI Demo functionality
"""
import asyncio
import os

import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def test_ai_chat():
    """Test the AI chat endpoint"""

    # Check if API key is set
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in environment variables")
        print("Please add OPENROUTER_API_KEY=your_api_key to your .env file")
        return False

    print("✅ OPENROUTER_API_KEY found")

    # Test the chat endpoint
    url = "http://localhost:8000/api/chat"
    payload = {
        "message": "Hello! Can you tell me a short joke?"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ Chat endpoint working!")
                    print(f"Response: {data.get('response', 'No response')}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Chat endpoint failed with status {response.status}")
                    print(f"Error: {error_text}")
                    return False
    except Exception as e:
        print(f"❌ Error testing chat endpoint: {e}")
        return False


async def test_ai_demo_page():
    """Test the AI demo page endpoint"""

    url = "http://localhost:8000/ai-demo"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    print("✅ AI demo page accessible!")
                    return True
                else:
                    print(f"❌ AI demo page failed with status {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Error testing AI demo page: {e}")
        return False


async def main():
    """Run all tests"""
    print("🧪 Testing AI Demo functionality...")
    print("=" * 50)

    # Test the demo page
    page_ok = await test_ai_demo_page()

    # Test the chat endpoint
    chat_ok = await test_ai_chat()

    print("=" * 50)
    if page_ok and chat_ok:
        print("🎉 All tests passed! AI Demo is ready to use.")
        print("Visit http://localhost:8000/ai-demo to try it out!")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())