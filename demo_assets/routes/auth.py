"""
Authentication routes
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from services.auth import create_user_token
from dependencies.database import get_db_session
from dependencies.config import get_settings, Settings
from fastapi_users.password import PasswordHelper

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page for webinar registrants access"""
    return templates.TemplateResponse("login.html", {
        "request": request,
        "title": "Login",
        "current_page": "login"
    })


@router.post("/login")
async def login_form(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings)
):
    """Handle login form submission using dependency injection with graceful database failure handling"""
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    if not username or not password:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "title": "Login",
            "current_page": "login",
            "error": "Please provide both email and password"
        })
    
    try:
        # Use injected database session
        result = await session.execute(
            select(User).where(User.email == username)
        )
        user = result.scalar_one_or_none()

        if not user:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "title": "Login",
                "current_page": "login",
                "error": "Invalid email or password"
            })

        password_helper = PasswordHelper()
        print(f"🔐 Password verification - Input password: {password}")
        print(f"🔐 Stored hash: {user.hashed_password}")
        print(f"🔐 User email: {user.email}")
        
        is_valid = password_helper.verify_and_update(str(password), user.hashed_password)
        print(f"🔐 Password verification result: {is_valid}")
        
        # verify_and_update returns (bool, str) - we need the first element
        if isinstance(is_valid, tuple):
            is_valid = is_valid[0]
        
        print(f"🔐 Final verification result: {is_valid}")
        
        if not is_valid:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "title": "Login",
                "current_page": "login",
                "error": "Invalid email or password"
            })

        if not user.is_active:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "title": "Login",
                "current_page": "login",
                "error": "Account is inactive"
            })

        if not (user.is_staff or user.is_superuser):
            return templates.TemplateResponse("login.html", {
                "request": request,
                "title": "Login",
                "current_page": "login",
                "error": "Access denied. Staff or admin privileges required."
            })

        # Create session token using unified auth system
        token = create_user_token(user)
        
        # Check if there's a redirect URL in the form or default to home
        redirect_url = form.get("next", "/")
        if not redirect_url.startswith("/"):
            redirect_url = "/"
        
        response = RedirectResponse(url=redirect_url, status_code=302)
        
        # Set cookie for application routes
        response.set_cookie(key="access_token", value=token, httponly=True, max_age=1800)  # 30 minutes
        
        # Also set session token for SQLAdmin
        request.session["token"] = token
        
        # Set session variables that SQLAdmin views check for
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
        
        print(f"🔐 Login form - JWT token created: {token[:20]}...")
        print(f"🔐 Login form - Cookie set: access_token={token[:20]}...")
        print(f"🔐 Login form - Session token set: {token[:20]}...")
        print(f"🔐 Login form - Session variables set: is_superuser={user.is_superuser}, "
              f"is_staff={user.is_staff}, group={user.group}")
        
        return response
        
    except Exception as e:
        print(f"Database error during login: {e}")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "title": "Login",
            "current_page": "login",
            "error": "Database is currently unavailable. Please check your database configuration and try again later."
        })


@router.get("/logout")
async def logout(request: Request):
    """Logout and clear authentication cookie and session"""
    # Clear all session variables
    request.session.pop("token", None)
    request.session.pop("is_authenticated", None)
    request.session.pop("is_superuser", None)
    request.session.pop("is_staff", None)
    request.session.pop("user_id", None)
    request.session.pop("user_email", None)
    request.session.pop("group", None)
    request.session.pop("can_manage_webinars", None)
    
    # Clear the access_token cookie (for application routes)
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="access_token")
    
    print("🔓 Logout endpoint - cleared all session variables and cookie tokens")
    return response
