import asyncio

from fastapi_users.password import PasswordHelper
from sqlmodel import select

from db import AsyncSessionLocal
from models import User


async def create_superuser():
    async with AsyncSessionLocal() as session:
        password_helper = PasswordHelper()
        password = "admin123"
        hashed_pw = password_helper.hash(password)
        
        # Check if superuser already exists
        result = await session.execute(
            select(User).where(User.email == "admin@example.com")
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            print("⚠️  Superuser already exists: admin@example.com")
            return
            
        user = User(
            email="admin@example.com",
            hashed_password=hashed_pw,
            is_active=True,
            is_superuser=True
        )
        session.add(user)
        await session.commit()
        print("✅ Superuser created: admin@example.com / admin123")

if __name__ == "__main__":
    asyncio.run(create_superuser())
