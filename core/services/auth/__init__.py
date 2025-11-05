"""
Unified Authentication Service
Provides JWT-based authentication for both SQLAdmin and application routes
"""
from .admin import AdminAuth
from .core import (
    create_user_token,
    get_current_staff_or_admin_from_authorization_header,
    get_current_staff_or_admin_from_cookies,
    get_current_superuser_from_authorization_header,
    get_current_superuser_from_cookies,
    get_current_user_from_authorization_header,
    get_current_user_from_cookies,
    get_secret_key,
    get_token_expire_minutes,
    verify_token,
)
from .dependencies import get_current_staff_or_admin, get_current_superuser, get_current_user

__all__ = [
    "create_user_token",
    "get_current_user_from_authorization_header",
    "get_current_staff_or_admin_from_authorization_header", 
    "get_current_superuser_from_authorization_header",
    "get_current_user_from_cookies", 
    "get_current_staff_or_admin_from_cookies",
    "get_current_superuser_from_cookies",
    "verify_token",
    "get_secret_key",
    "get_token_expire_minutes",
    "AdminAuth",
    "get_current_user",
    "get_current_staff_or_admin", 
    "get_current_superuser"
]
