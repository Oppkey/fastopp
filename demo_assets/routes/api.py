"""
API routes for data endpoints
"""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from models import User
from core.services.auth import get_current_staff_or_admin
from dependencies.services import get_product_service

router = APIRouter()


@router.get("/products")
async def get_products(product_service = Depends(get_product_service)):
    """API endpoint to fetch product data for the dashboard"""
    data = await product_service.get_products_with_stats()
    return JSONResponse(data)


@router.get("/registrants")
async def get_registrants(current_user: User = Depends(get_current_staff_or_admin)):
    """Get all webinar registrants with their photos"""
    from services.webinar_service import WebinarService
    
    registrants = await WebinarService.get_all_registrants()
    return JSONResponse({"registrants": registrants})


@router.get("/webinar-attendees")
async def get_webinar_attendees(request: Request):
    """Get webinar attendees for the marketing demo page"""
    from services.webinar_service import WebinarService
    from fastapi.templating import Jinja2Templates
    
    attendees = await WebinarService.get_webinar_attendees()
    
    # Check if this is an HTMX request
    templates = Jinja2Templates(directory="templates")
    
    # Return HTML for HTMX requests, JSON for API requests
    if 'hx-request' in request.headers:
        return templates.TemplateResponse("partials/attendees-grid.html", {
            "request": request,
            "attendees": attendees
        })
    else:
        return JSONResponse({"attendees": attendees}) 