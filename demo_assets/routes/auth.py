"""
Authentication routes
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from dependencies.auth import create_user_token
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
    """Handle login form submission using dependency injection"""
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

    # Create session token using dependency injection
    token = create_user_token(user, settings)
    
    # Check if there's a redirect URL in the form or default to home
    redirect_url = form.get("next", "/")
    if not redirect_url.startswith("/"):
        redirect_url = "/"
    
    response = RedirectResponse(url=redirect_url, status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=1800)  # 30 minutes
    return response


@router.get("/logout")
async def logout():
    """Logout and clear authentication cookie"""
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="access_token")
    return response 