# =========================
# admin/views.py (Base Assets - Users Only)
# =========================
from typing import Any
from sqladmin import ModelView
from models import User


class UserAdmin(ModelView, model=User):
    column_list = ["email", "is_active", "is_superuser", "is_staff", "group"]
    
    def is_accessible(self, request: Any) -> bool:
        """Only superusers can manage users"""
        return request.session.get("is_superuser", False)
    
    def is_visible(self, request: Any) -> bool:
        """Only show user management to superusers"""
        return request.session.get("is_superuser", False)
