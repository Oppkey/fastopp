"""
SQLAdmin Authentication Backend
Integrates SQLAdmin login with unified JWT authentication system
"""
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi_users.password import PasswordHelper
from sqlmodel import select
from db import AsyncSessionLocal
from models import User
from sqladmin.authentication import AuthenticationBackend
from .core import create_user_token, get_secret_key


class AdminAuth(AuthenticationBackend):
    """SQLAdmin authentication backend that integrates with unified JWT system"""
    
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)

    async def login(self, request: Request) -> bool:
        """Handle admin login and create JWT token"""
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
                # Create JWT token for unified authentication
                token = create_user_token(user)
                
                # Set the JWT token as a cookie for application authentication
                response = RedirectResponse(url="/admin", status_code=302)
                response.set_cookie(
                    key="access_token", 
                    value=token, 
                    httponly=True, 
                    max_age=1800,  # 30 minutes
                    secure=False,  # Set to True in production with HTTPS
                    samesite="lax"
                )
                
                # Store the response in request state for SQLAdmin to use
                request.state.auth_response = response
                
                return True
            
            return False

    async def logout(self, request: Request) -> bool:
        """Handle admin logout and clear JWT token"""
        # Clear the JWT token cookie
        response = RedirectResponse(url="/admin/login", status_code=302)
        response.delete_cookie(key="access_token")
        
        # Store the response in request state for SQLAdmin to use
        request.state.auth_response = response
        
        return True

    async def authenticate(self, request: Request) -> bool:
        """Check if user is authenticated using JWT token"""
        try:
            from .core import get_current_user_from_cookies
            user = await get_current_user_from_cookies(request)
            return user is not None and (user.is_staff or user.is_superuser)
        except:
            return False
