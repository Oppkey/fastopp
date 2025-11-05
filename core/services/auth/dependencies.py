"""
FastAPI Dependencies for Authentication
Provides dependency injection support for demo mode
"""
from fastapi import Depends, Request

from models import User

from .core import (
    get_current_staff_or_admin_from_cookies,
    get_current_superuser_from_cookies,
    get_current_user_from_cookies,
)


async def get_current_user(request: Request) -> User:
    """FastAPI dependency to get current authenticated user"""
    return await get_current_user_from_cookies(request)


async def get_current_staff_or_admin(request: Request) -> User:
    """FastAPI dependency to get current user with staff or admin privileges"""
    return await get_current_staff_or_admin_from_cookies(request)


async def get_current_superuser(request: Request) -> User:
    """FastAPI dependency to get current user with superuser privileges"""
    return await get_current_superuser_from_cookies(request)
