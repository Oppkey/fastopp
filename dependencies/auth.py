"""
Authentication dependencies for dependency injection
"""
from datetime import datetime, timedelta
from typing import Optional
import uuid

from fastapi import Depends, HTTPException, Request, status
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import User

from .config import Settings, get_settings
from .database import get_db_session


def create_access_token(
    data: dict,
    settings: Settings = Depends(get_settings)
) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")


def verify_token(
    token: str,
    settings: Settings = Depends(get_settings)
) -> Optional[dict]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        return None


async def get_current_user_from_cookies(
    request: Request,
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings)
) -> User:
    """Get current authenticated user from cookies using dependency injection"""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify JWT token
    payload = verify_token(token, settings)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

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

    # Get user from database using injected session
    result = await session.execute(select(User).where(User.id == user_uuid))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_staff_or_admin(
    current_user: User = Depends(get_current_user_from_cookies)
) -> User:
    """Get current authenticated user with staff or admin privileges"""
    if not (current_user.is_staff or current_user.is_superuser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff or admin privileges required",
        )
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user_from_cookies)
) -> User:
    """Get current authenticated user with superuser privileges"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser privileges required",
        )
    return current_user


def create_user_token(user: User, settings: Settings = Depends(get_settings)) -> str:
    """Create a JWT token for the user using dependency injection"""
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser
    }
    return create_access_token(token_data, settings)
