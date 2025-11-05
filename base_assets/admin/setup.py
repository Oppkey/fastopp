# =========================
# admin/setup.py (Base Assets - Users Only)
# =========================
import os

from fastapi import FastAPI
from sqladmin import Admin

from core.services.auth import AdminAuth
from db import async_engine

from .views import UserAdmin


def setup_admin(app: FastAPI, secret_key: str):
    """Setup and configure the admin interface for base application (Users only)"""
    # Check if we're in production (HTTPS environment)
    is_production = (os.getenv("RAILWAY_ENVIRONMENT") or
                     os.getenv("PRODUCTION") or
                     os.getenv("FORCE_HTTPS") or
                     os.getenv("ENVIRONMENT") == "production" or
                     os.getenv("LEAPCELL_ENVIRONMENT") or
                     "leapcell" in os.getenv("DATABASE_URL", "").lower())

    # Configure admin with HTTPS support for production
    if is_production:
        admin = Admin(
            app=app,
            engine=async_engine,
            authentication_backend=AdminAuth(secret_key=secret_key),
            base_url="/admin",
            title="FastOpp Admin",
            logo_url=None,  # Disable logo to avoid mixed content issues
        )
    else:
        admin = Admin(
            app=app,
            engine=async_engine,
            authentication_backend=AdminAuth(secret_key=secret_key)
        )

    # Register admin views (Users only for base application)
    admin.add_view(UserAdmin)
    return admin
