"""
Authentication routes for base_assets
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from db import AsyncSessionLocal
from models import User
from core.services.auth import create_user_token
from fastapi_users.password import PasswordHelper

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page for accessing protected content"""
    return templates.TemplateResponse("login.html", {
        "request": request,
        "title": "Login",
        "current_page": "login"
    })


@router.post("/login")
async def login_form(request: Request):
    """Handle login form submission"""
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
    
    async with AsyncSessionLocal() as session:
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
        is_valid = password_helper.verify_and_update(str(password), user.hashed_password)
        
        # verify_and_update returns (bool, str) - we need the first element
        if hasattr(is_valid, '__getitem__'):
            is_valid = is_valid[0]
        
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

        # Create session token
        token = create_user_token(user)
        
        # Set session variables for SQLAdmin (same as SQLAdmin login)
        request.session["token"] = token
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
        
        response = RedirectResponse(url="/protected", status_code=302)
        response.set_cookie(key="access_token", value=token, httponly=True, max_age=1800)  # 30 minutes
        return response


@router.get("/logout")
async def logout(request: Request):
    """Logout and clear authentication cookie and session data"""
    # Clear all session variables (same as SQLAdmin logout)
    request.session.pop("token", None)
    request.session.pop("is_authenticated", None)
    request.session.pop("is_superuser", None)
    request.session.pop("is_staff", None)
    request.session.pop("user_id", None)
    request.session.pop("user_email", None)
    request.session.pop("group", None)
    request.session.pop("can_manage_webinars", None)
    
    # Clear the JWT token cookie
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="access_token")
    return response
