#!/usr/bin/env python3
"""
Script to test the authentication system
"""

import asyncio
from core.services.auth import create_user_token
from db import AsyncSessionLocal
from models import User
from sqlmodel import select


async def test_auth():
    """Test the authentication system"""
    # Test with a staff user
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.email == "staff@example.com")
        )
        user = result.scalar_one_or_none()
        
        if user:
            print(f"Testing with user: {user.email}")
            print(f"Staff: {user.is_staff}, Superuser: {user.is_superuser}")
            
            # Create token
            token = create_user_token(user)
            print(f"Token created: {token[:50]}...")
            
            # Simple token validation (check format)
            if token.startswith("token_") and str(user.id) in token:
                print(f"Token format valid, contains user_id: {user.id}")
            else:
                print("Token format invalid")
        else:
            print("User not found")


if __name__ == "__main__":
    asyncio.run(test_auth()) 