"""
Webinar registrant management routes
"""
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import HTMLResponse

from core.services.auth import get_current_staff_or_admin
from models import User

router = APIRouter()


@router.post("/upload-photo/{registrant_id}")
async def upload_photo(
    registrant_id: str,
    photo: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_staff_or_admin)
):
    """Upload a photo for a webinar registrant"""
    
    # Validate file type
    if not photo.content_type or not photo.content_type.startswith('image/'):
        return HTMLResponse(
            '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">'
            'Error: File must be an image</div>',
            status_code=400
        )
    
    # Validate file size (max 5MB)
    if photo.size and photo.size > 5 * 1024 * 1024:
        return HTMLResponse(
            '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">'
            'Error: File size must be less than 5MB</div>',
            status_code=400
        )
    
    # Read file content
    content = await photo.read()
    
    # Use service to handle upload
    from services.webinar_service import WebinarService
    success, message, _ = await WebinarService.upload_photo(
        registrant_id, content, photo.filename or "photo.jpg"
    )
    
    if success:
        return HTMLResponse(
            '<div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">'
            f'{message}</div>'
        )
    else:
        return HTMLResponse(
            f'<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">'
            f'Error: {message}</div>',
            status_code=400
        )


@router.post("/update-notes/{registrant_id}")
async def update_notes(
    registrant_id: str,
    notes: str = Form(...)
):
    """Update notes for a webinar registrant"""
    from services.webinar_service import WebinarService
    
    success, message = await WebinarService.update_notes(registrant_id, notes)
    
    if success:
        return HTMLResponse(
            '<div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">'
            f'{message}</div>'
        )
    else:
        return HTMLResponse(
            f'<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">'
            f'Error: {message}</div>',
            status_code=400
        )


@router.delete("/delete-photo/{registrant_id}")
async def delete_photo(registrant_id: str):
    """Delete a photo for a webinar registrant"""
    from services.webinar_service import WebinarService
    
    success, message = await WebinarService.delete_photo(registrant_id)
    
    if success:
        return HTMLResponse(
            '<div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">'
            f'{message}</div>'
        )
    else:
        return HTMLResponse(
            f'<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">'
            f'Error: {message}</div>',
            status_code=400
        ) 