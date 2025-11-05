"""
Page routes for rendering HTML templates
"""
import os

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.services.auth import get_current_staff_or_admin, get_current_user_from_cookies
from core.services.template_context import get_template_context
from models import User

templates = Jinja2Templates(directory="templates")

router = APIRouter()


def format_model_name(model_identifier: str) -> str:
    """
    Format a model identifier into a more human-readable display name

    Args:
        model_identifier: The model identifier
            (e.g., "meta-llama/llama-3.3-70b-instruct:free")

    Returns:
        str: A formatted display name
            (e.g., "Llama 3.3 70B Instruct (Free)")
    """
    # Extract the model name part (after the slash)
    if '/' in model_identifier:
        model_name = model_identifier.split('/', 1)[1]
    else:
        model_name = model_identifier

    # Check if it has a :free suffix
    is_free = model_name.endswith(':free')
    if is_free:
        model_name = model_name[:-5]  # Remove ':free'

    # Format common model patterns
    # Handle llama models
    if 'llama' in model_name.lower():
        # Extract version and size info
        parts = model_name.replace('llama-', '').split('-')
        formatted_parts = []
        for part in parts:
            if part.replace('.', '').isdigit():  # Version number
                formatted_parts.append(part)
            # Size like "70b"
            elif 'b' in part.lower() and part[:-1].isdigit():
                formatted_parts.append(part.upper())
            else:
                formatted_parts.append(part.capitalize())

        display = f"Llama {' '.join(formatted_parts)}"
    # Handle OpenAI models
    elif 'gpt' in model_name.lower():
        display = model_name.upper().replace('-', ' ').title()
    # Handle Qwen models
    elif 'qwen' in model_name.lower():
        display = model_name.replace('-', ' ').title()
    else:
        # Generic formatting
        display = model_name.replace('-', ' ').replace('_', ' ').title()

    # Add "(Free)" suffix if applicable
    if is_free:
        display += " (Free)"

    return display


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Home page"""
    # Get authentication context
    auth_context = get_template_context(request)
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "title": "Delightful Demo Dashboard",
        **auth_context
    })


@router.get("/design-demo", response_class=HTMLResponse)
async def design_demo(request: Request):
    """Design demo page"""
    return templates.TemplateResponse("design-demo.html", {"request": request, "title": "FastOpp Design Demo"})


@router.get("/auth-test", response_class=HTMLResponse)
async def auth_test(request: Request):
    """Test authentication state"""
    auth_context = get_template_context(request)
    
    return templates.TemplateResponse("auth-test.html", {
        "request": request,
        "title": "Authentication Test",
        **auth_context
    })


@router.get("/database-demo", response_class=HTMLResponse)
async def database_demo(request: Request):
    """Product database demo page"""
    return templates.TemplateResponse("database-demo.html", {"request": request, "title": "Product Database Demo"})


@router.get("/webinar-registrants", response_class=HTMLResponse)
async def webinar_registrants(request: Request, current_user: User = Depends(get_current_staff_or_admin)):
    """Webinar registrants management page"""
    return templates.TemplateResponse("webinar-registrants.html", {
        "request": request,
        "title": "Webinar Registrants",
        "current_page": "webinar-registrants"
    })


@router.get("/webinar-demo", response_class=HTMLResponse)
async def webinar_demo(request: Request):
    """Marketing page showcasing webinar attendees and community"""
    return templates.TemplateResponse("webinar-demo.html", {
        "request": request,
        "title": "Webinar Demo",
        "current_page": "webinar-demo"
    })


@router.get("/ai-demo", response_class=HTMLResponse)
async def ai_demo(request: Request):
    """AI Chat demo page with LLM integration"""
    # Get the LLM model from environment (same default as chat_service.py)
    llm_model = os.getenv(
        "OPENROUTER_LLM_MODEL",
        "meta-llama/llama-3.3-70b-instruct:free"
    )
    llm_model_display = format_model_name(llm_model)

    return templates.TemplateResponse("ai-demo.html", {
        "request": request,
        "title": "AI Chat Demo",
        "current_page": "ai-demo",
        "llm_model": llm_model,
        "llm_model_display": llm_model_display
    })


@router.get("/ai-stats", response_class=HTMLResponse)
async def ai_stats(request: Request):
    """HTMX endpoint to return AI marketing statistics"""
    import time
    time.sleep(1)  # Simulate processing time

    stats = [
        {"metric": "Content Generation Speed", "value": "10x Faster", "icon": "⚡"},
        {"metric": "Campaign ROI", "value": "+340%", "icon": "📈"},
        {"metric": "Time Saved", "value": "87%", "icon": "⏰"},
        {"metric": "Engagement Rate", "value": "+280%", "icon": "🎯"}
    ]

    return templates.TemplateResponse("partials/ai-stats.html", {
        "request": request,
        "stats": stats
    })


@router.post("/marketing-demo", response_class=HTMLResponse)
async def marketing_demo(request: Request):
    """HTMX endpoint to handle marketing demo form submission"""
    # In a real app, you'd parse form data properly
    # For demo purposes, we'll simulate form processing
    import time
    time.sleep(1.5)  # Simulate processing time

    return templates.TemplateResponse("partials/demo-response.html", {
        "request": request,
        "success": True,
        "message": "Thank you! Our AI team will contact you within 24 hours with a personalized marketing demo."
    })


@router.get("/license")
async def license_page(request: Request):
    """License page"""
    return templates.TemplateResponse("license.html", {
        "request": request,
        "title": "MIT License"
    })


@router.get("/database-status")
async def database_status_page(request: Request):
    """Database status page for troubleshooting"""
    from dependencies.database_health import get_database_status
    
    status = await get_database_status()
    
    return templates.TemplateResponse("database-status.html", {
        "request": request,
        "title": "Database Status",
        "status": status
    })