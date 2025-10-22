# =========================
# admin/setup.py (Demo Assets - Full Features)
# =========================
import os
from sqladmin import Admin
from fastapi import FastAPI
from dependencies.database import create_database_engine
from dependencies.config import get_settings
from core.services.auth import AdminAuth
from .views import UserAdmin, ProductAdmin, WebinarRegistrantsAdmin, AuditLogAdmin


def setup_admin(app: FastAPI, secret_key: str):
    """Setup and configure the admin interface for demo application (all features)"""
    print("🔧 Setting up SQLAdmin with unified authentication")
    
    # Get settings and create database engine using dependency injection
    settings = get_settings()
    engine = create_database_engine(settings)

    # Check if we're in production (HTTPS environment)
    is_production = (os.getenv("RAILWAY_ENVIRONMENT") or
                     os.getenv("PRODUCTION") or
                     os.getenv("FORCE_HTTPS") or
                     os.getenv("ENVIRONMENT") == "production" or
                     os.getenv("LEAPCELL_ENVIRONMENT") or
                     "leapcell" in os.getenv("DATABASE_URL", "").lower())

    # Create authentication backend
    auth_backend = AdminAuth(secret_key=secret_key)
    print(f"🔧 Created AdminAuth backend: {auth_backend}")
    
    # Configure admin with HTTPS support for production
    if is_production:
        admin = Admin(
            app=app,
            engine=engine,
            authentication_backend=auth_backend,
            base_url="/admin",
            title="FastOpp Admin",
            logo_url=None,  # Disable logo to avoid mixed content issues
        )
    else:
        admin = Admin(
            app=app,
            engine=engine,
            authentication_backend=auth_backend
        )
    
    print(f"🔧 SQLAdmin created with authentication: {admin.authentication_backend}")

    # Register admin views (all features for demo application)
    admin.add_view(UserAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(WebinarRegistrantsAdmin)
    admin.add_view(AuditLogAdmin)
    return admin