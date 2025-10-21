"""
SQLAdmin authentication backend for base_assets
Simple version without dependency injection
"""
from fastapi import Request
from fastapi_users.password import PasswordHelper
from sqlmodel import select
from db import AsyncSessionLocal
from models import User
from sqladmin.authentication import AuthenticationBackend


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)

    async def login(self, request: Request) -> bool:
        """Handle admin login"""
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if not username or not password:
            return False

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.email == username)
            )
            user = result.scalar_one_or_none()

            if not user:
                return False

            if not user.is_active:
                return False

            if not (user.is_staff or user.is_superuser):
                return False

            password_helper = PasswordHelper()
            is_valid = password_helper.verify_and_update(str(password), user.hashed_password)
            
            # verify_and_update returns (bool, str) - we need the first element
            if hasattr(is_valid, '__getitem__'):
                is_valid = is_valid[0]
            
            if is_valid:
                # Set session data for authentication
                request.session["is_authenticated"] = True
                request.session["user_id"] = str(user.id)
                request.session["user_email"] = user.email
                request.session["is_superuser"] = user.is_superuser
                request.session["is_staff"] = user.is_staff
                request.session["group"] = user.group
                request.session["can_manage_webinars"] = user.is_superuser or user.group in ["marketing", "sales"]
            
            return is_valid

    async def logout(self, request: Request) -> bool:
        """Handle admin logout"""
        # Clear session data
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Check if user is authenticated"""
        # Check if user has a valid session
        session = request.session
        return session.get("is_authenticated", False)
