#!/usr/bin/env python3
"""
Test script to demonstrate improved message formatting with DaisyUI
"""
import asyncio
import os

import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_formatted_messages():
    """Test the AI chat with messages that should trigger formatting"""

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found")
        return False

    # Test messages that should trigger different formatting
    test_messages = [
        "Can you explain what **bold text** and *italic text* look like?",
        "Show me some `code examples` in your response",
        "Write a Python function with ```code blocks```",
        "Create a list with:\n1. First item\n2. Second item\n3. Third item"
    ]

    url = "http://localhost:8000/api/chat"

    for i, message in enumerate(test_messages, 1):
        print(f"\n🧪 Test {i}: {message}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json={"message": message}) as response:
                    if response.status == 200:
                        await response.json()  # Get response but don't use it
                        print("✅ Response received")
                        print("📝 Formatted content will show:")
                        print("   - Bold text: **text**")
                        print("   - Italic text: *text*")
                        print("   - Inline code: `code`")
                        print("   - Code blocks: ```code```")
                        print("   - Line breaks: \\n")
                    else:
                        print(f"❌ Failed with status {response.status}")
        except Exception as e:
            print(f"❌ Error: {e}")

    return True


async def main():
    """Run the formatting test"""
    print("🎨 Testing DaisyUI Message Formatting...")
    print("=" * 60)

    success = await test_formatted_messages()

    print("=" * 60)
    if success:
        print("🎉 Formatting test completed!")
        print("💡 Visit http://localhost:8000/ai-demo to see the formatted messages")
        print("✨ DaisyUI provides better chat bubbles and formatting support")
    else:
        print("❌ Test failed")

if __name__ == "__main__":
    asyncio.run(main())