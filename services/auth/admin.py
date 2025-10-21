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
from .core import create_user_token


class AdminAuth(AuthenticationBackend):
    """SQLAdmin authentication backend that integrates with unified JWT system"""

    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)

    async def login(self, request: Request) -> bool:
        """Handle admin login and create JWT token"""
        print("🔐 SQLAdmin login called")
        print(f"🔐 Request URL: {request.url}")
        print(f"🔐 Request method: {request.method}")

        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        print(f"🔐 Username: {username}")
        print(f"🔐 Password provided: {bool(password)}")

        if not username or not password:
            print("🔐 Missing username or password")
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
                # SQLAdmin will use this via the authenticate() method
                request.session["token"] = token  # SQLAdmin session

                # Set session variables that admin views check for
                request.session["is_authenticated"] = True
                request.session["is_superuser"] = user.is_superuser
                request.session["is_staff"] = user.is_staff
                request.session["user_id"] = str(user.id)
                request.session["user_email"] = user.email
                request.session["group"] = user.group

                # Set additional permissions based on user group
                if user.group == "marketing":
                    request.session["can_manage_webinars"] = True
                elif user.group == "sales":
                    request.session["can_manage_webinars"] = True
                elif user.is_superuser:
                    request.session["can_manage_webinars"] = True
                else:
                    request.session["can_manage_webinars"] = False

                # Also set as access_token cookie for application routes
                response = RedirectResponse(url="/admin", status_code=302)
                response.set_cookie(
                    key="access_token",
                    value=token,
                    httponly=True,
                    max_age=1800,  # 30 minutes
                    secure=False,  # Set to True in production with HTTPS
                    samesite="lax",
                    path="/"  # Make cookie available for entire site
                )

                # Store the response in request state for SQLAdmin to use
                request.state.auth_response = response

                print(f"🔐 Login successful for user: {user.email}")
                print(f"🔐 JWT token created: {token[:20]}...")
                print(f"🔐 Cookie set: access_token={token[:20]}...")
                print(f"🔐 Session variables set: is_superuser={user.is_superuser}, "
                      f"is_staff={user.is_staff}, group={user.group}")
                return True

            return False

    async def logout(self, request: Request) -> bool:
        """Handle admin logout and clear JWT token"""
        print("🔓 SQLAdmin logout called - clearing JWT token")
        print(f"🔓 Request URL: {request.url}")
        print(f"🔓 Request method: {request.method}")
        print(f"🔓 Request headers: {dict(request.headers)}")

        # Clear all session variables
        request.session.pop("token", None)
        request.session.pop("is_authenticated", None)
        request.session.pop("is_superuser", None)
        request.session.pop("is_staff", None)
        request.session.pop("user_id", None)
        request.session.pop("user_email", None)
        request.session.pop("group", None)
        request.session.pop("can_manage_webinars", None)

        # Clear the JWT token cookie
        response = RedirectResponse(url="/admin/login", status_code=302)
        response.delete_cookie(key="access_token")

        # Store the response in request state for SQLAdmin to use
        request.state.auth_response = response

        print("🔓 JWT token and all session variables cleared")
        return True

    async def get_user(self, request: Request):
        """Get current user for SQLAdmin"""
        try:
            from .core import get_current_user_from_cookies
            user = await get_current_user_from_cookies(request)
            if user and (user.is_staff or user.is_superuser):
                return user
            return None
        except Exception:
            return None

    async def authenticate(self, request: Request) -> bool:
        """Check if user is authenticated using JWT token"""
        try:
            # Check if there's a session token
            token = request.session.get("token")
            if not token:
                # Fall back to cookie-based authentication
                from .core import get_current_user_from_cookies
                user = await get_current_user_from_cookies(request)
                return user is not None and (user.is_staff or user.is_superuser)

            # Verify the session token
            from .core import verify_token
            payload = verify_token(token)
            if not payload:
                return False

            # Check if user is staff or superuser
            return payload.get("is_staff") or payload.get("is_superuser")
        except Exception as e:
            print(f"🔐 Authentication error: {e}")
            return False
