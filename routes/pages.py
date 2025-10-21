"""
Page routes for base_assets
"""
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from base_assets.auth.core import get_current_staff_or_admin_from_cookies
from models import User

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Home page with links to protected content"""
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "title": "Welcome to FastOpp Base Assets"
    })


@router.get("/protected", response_class=HTMLResponse)
async def protected_page(request: Request, current_user: User = Depends(get_current_staff_or_admin_from_cookies)):
    """Protected page that requires authentication"""
    return templates.TemplateResponse("protected.html", {
        "request": request, 
        "title": "Protected Content",
        "current_page": "protected",
        "user": current_user
    })
