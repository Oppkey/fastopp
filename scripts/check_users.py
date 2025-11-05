#!/usr/bin/env python3
"""
Script to check existing users and their permissions
"""

import asyncio

from sqlmodel import select

from db import AsyncSessionLocal
from models import User


async def check_users():
    """Check existing users and their permissions"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        print(f"Found {len(users)} users:")
        for user in users:
            print(f"- {user.email} (staff: {user.is_staff}, superuser: {user.is_superuser})")


if __name__ == "__main__":
    asyncio.run(check_users()) 