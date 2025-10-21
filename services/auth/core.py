"""
Unified Authentication Core
JWT-based authentication system for both SQLAdmin and application routes
"""
import uuid
import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Request, status
from fastapi_users.password import PasswordHelper
from sqlmodel import select
from db import AsyncSessionLocal
from models import User
import jwt


def get_secret_key() -> str:
    """Get secret key from environment"""
    return os.getenv("SECRET_KEY", "dev_secret_key_change_in_production")


def get_token_expire_minutes() -> int:
    """Get token expiration time from environment"""
    return int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def create_user_token(user: User) -> str:
    """Create a JWT token for the user"""
    secret_key = get_secret_key()
    expire_minutes = get_token_expire_minutes()
    
    # Create JWT payload
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "exp": datetime.utcnow() + timedelta(minutes=expire_minutes)
    }
    
    # Create JWT token
    return jwt.encode(token_data, secret_key, algorithm="HS256")


def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload"""
    secret_key = get_secret_key()
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        return None


async def get_current_user_from_cookies(request: Request) -> User:
    """Get current authenticated user from cookies using JWT"""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify JWT token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user ID from JWT payload
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_uuid))
        user = result.scalar_one_or_none()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user


async def get_current_staff_or_admin_from_cookies(request: Request) -> User:
    """Get current authenticated user with staff or admin privileges"""
    user = await get_current_user_from_cookies(request)
    
    if not (user.is_staff or user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff or admin privileges required",
        )
    
    return user


async def get_current_superuser_from_cookies(request: Request) -> User:
    """Get current authenticated user with superuser privileges"""
    user = await get_current_user_from_cookies(request)
    
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser privileges required",
        )
    
    return user
