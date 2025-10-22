"""
Template context processor for authentication state
"""
from fastapi import Request
from services.auth import get_current_user_from_cookies
from models import User
from typing import Optional


async def get_auth_context(request: Request) -> dict:
    """
    Get authentication context for templates
    Returns authentication state that can be used in templates
    """
    try:
        # Try to get current user using the sophisticated auth system
        user = await get_current_user_from_cookies(request)
        return {
            "is_authenticated": True,
            "current_user": user,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
            "user_email": user.email,
            "user_group": user.group
        }
    except Exception:
        # If authentication fails, return unauthenticated state
        return {
            "is_authenticated": False,
            "current_user": None,
            "is_superuser": False,
            "is_staff": False,
            "user_email": None,
            "user_group": None
        }


def get_template_context(request: Request, **kwargs) -> dict:
    """
    Synchronous template context processor
    This is called by Jinja2Templates for every template render
    """
    # Check for access_token cookie as fallback
    has_access_token = bool(request.cookies.get('access_token'))
    
    # Check for session token as fallback
    has_session_token = bool(request.session.get('token'))
    
    # Basic authentication state
    auth_state = {
        "is_authenticated": has_access_token or has_session_token,
        "has_access_token": has_access_token,
        "has_session_token": has_session_token,
        "current_user": None,
        "is_superuser": False,
        "is_staff": False,
        "user_email": None,
        "user_group": None
    }
    
    # Add session data if available
    if has_session_token:
        auth_state.update({
            "is_superuser": request.session.get('is_superuser', False),
            "is_staff": request.session.get('is_staff', False),
            "user_email": request.session.get('user_email'),
            "user_group": request.session.get('group')
        })
    
    # Merge with any additional context
    auth_state.update(kwargs)
    
    return auth_state
