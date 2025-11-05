# =========================
# add_test_users.py - Add test users to database
# =========================
import asyncio

from fastapi_users.password import PasswordHelper
from sqlmodel import select

from db import AsyncSessionLocal
from models import User


async def add_test_users():
    """Add test users to the database"""
    async with AsyncSessionLocal() as session:
        password_helper = PasswordHelper()
        password = "test123"
        hashed_pw = password_helper.hash(password)
        
        # Add several test users with different groups and permissions
        test_users = [
            {
                "email": "john@example.com",
                "hashed_password": hashed_pw,
                "is_active": True,
                "is_superuser": False,
                "is_staff": True,
                "group": "marketing"  # Marketing can manage webinars
            },
            {
                "email": "jane@example.com", 
                "hashed_password": hashed_pw,
                "is_active": True,
                "is_superuser": False,
                "is_staff": True,
                "group": "sales"  # Sales can view assigned webinars
            },
            {
                "email": "bob@example.com",
                "hashed_password": hashed_pw,
                "is_active": False,  # Inactive user
                "is_superuser": False,
                "is_staff": False,
                "group": None
            },
            {
                "email": "admin2@example.com",
                "hashed_password": hashed_pw,
                "is_active": True,
                "is_superuser": True,  # Superuser - full access
                "is_staff": True,
                "group": "admin"
            },
            {
                "email": "staff@example.com",
                "hashed_password": hashed_pw,
                "is_active": True,
                "is_superuser": False,
                "is_staff": True,
                "group": "support"  # Support can only view products
            },
            {
                "email": "marketing@example.com",
                "hashed_password": hashed_pw,
                "is_active": True,
                "is_superuser": False,
                "is_staff": True,
                "group": "marketing"  # Marketing can manage webinars
            },
            {
                "email": "sales@example.com",
                "hashed_password": hashed_pw,
                "is_active": True,
                "is_superuser": False,
                "is_staff": True,
                "group": "sales"  # Sales can view assigned webinars
            }
        ]
        
        for user_data in test_users:
            # Skip if user already exists (idempotent)
            result = await session.execute(select(User).where(User.email == user_data["email"]))
            if result.scalar_one_or_none():
                print(f"ℹ️  User already exists, skipping: {user_data['email']}")
                continue
            user = User(**user_data)
            session.add(user)
        
        await session.commit()
        print("✅ Added test users to database (skipping existing users)")
        print("Test users:")
        print("- admin@example.com (superuser, admin) - created by superuser script")
        print("- admin2@example.com (superuser, admin)")
        print("- john@example.com (staff, marketing)")
        print("- jane@example.com (staff, sales)")
        print("- staff@example.com (staff, support)")
        print("- marketing@example.com (staff, marketing)")
        print("- sales@example.com (staff, sales)")
        print("- bob@example.com (inactive)")
        print("All users have password: test123")
        print("\nPermission levels:")
        print("- Superusers: Full admin access (users + products + webinars + audit)")
        print("- Marketing: Product management + webinar management")
        print("- Sales: Product management + assigned webinar viewing")
        print("- Support: Product management only")
        print("- Regular users: No admin access")


if __name__ == "__main__":
    asyncio.run(add_test_users()) 