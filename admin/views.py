# =========================
# admin/views.py (Demo Assets - Full Features)
# =========================
from typing import Any
from sqladmin import ModelView
from models import User, Product, WebinarRegistrants, AuditLog


class UserAdmin(ModelView, model=User):
    column_list = ["email", "is_active", "is_superuser", "is_staff", "group"]
    
    def is_accessible(self, request: Any) -> bool:
        """Only superusers can manage users"""
        return request.session.get("is_superuser", False)
    
    def is_visible(self, request: Any) -> bool:
        """Only show user management to superusers"""
        return request.session.get("is_superuser", False)


class ProductAdmin(ModelView, model=Product):
    column_list = ["name", "price", "category", "in_stock", "created_at"]
    column_searchable_list = ["name", "description", "category"]
    
    def is_accessible(self, request: Any) -> bool:
        """Staff and superusers can manage products"""
        return request.session.get("is_superuser", False) or request.session.get("is_staff", False)
    
    def can_create(self, request: Any) -> bool:
        """Only superusers can create products"""
        return request.session.get("is_superuser", False)
    
    def can_delete(self, request: Any) -> bool:
        """Only superusers can delete products"""
        return request.session.get("is_superuser", False)


class WebinarRegistrantsAdmin(ModelView, model=WebinarRegistrants):
    column_list = ["name", "email", "company", "webinar_title", "webinar_date", "status", "group", "notes"]
    column_searchable_list = ["name", "email", "company", "webinar_title", "notes"]
    
    def is_accessible(self, request: Any) -> bool:
        """Webinar managers and superusers can access registrants"""
        return (request.session.get("is_superuser", False) or 
                request.session.get("can_manage_webinars", False))
    
    def can_create(self, request: Any) -> bool:
        """Only marketing and superusers can create registrations"""
        return (request.session.get("is_superuser", False) or 
                request.session.get("group") == "marketing")
    
    def can_edit(self, request: Any) -> bool:
        """Marketing, sales (for assigned), and superusers can edit"""
        if request.session.get("is_superuser", False):
            return True
        if request.session.get("group") == "marketing":
            return True
        if request.session.get("group") == "sales":
            # Sales can only edit their assigned registrants
            return True  # Filtering handled in get_query
        return False


class AuditLogAdmin(ModelView, model=AuditLog):
    column_list = ["user_id", "action", "model_name", "record_id", "timestamp"]
    column_searchable_list = ["action", "model_name", "record_id"]
    can_create = False  # Audit logs are read-only
    can_edit = False
    can_delete = False
    
    def is_accessible(self, request: Any) -> bool:
        """Only superusers can view audit logs"""
        return request.session.get("is_superuser", False)
    
    def is_visible(self, request: Any) -> bool:
        """Only show audit logs to superusers"""
        return request.session.get("is_superuser", False)
