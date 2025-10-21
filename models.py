# =========================
# demo_assets/models.py
# Full models for demo_assets - all models
# =========================
import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)  # New field for staff permissions
    group: Optional[str] = Field(default=None)  # marketing, sales, support, etc.


class Product(SQLModel, table=True):
    __tablename__ = "products"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    price: float = Field(nullable=False)
    category: Optional[str] = Field(max_length=50, default=None, nullable=True)
    in_stock: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WebinarRegistrants(SQLModel, table=True):
    __tablename__ = "webinar_registrants"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    company: Optional[str] = Field(max_length=100, default=None, nullable=True)
    webinar_title: str = Field(max_length=200, nullable=False)
    webinar_date: datetime = Field(nullable=False)
    registration_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = Field(default="registered")  # registered, attended, cancelled, no_show
    assigned_sales_rep: Optional[str] = Field(default=None, nullable=True)
    group: Optional[str] = Field(default=None)  # marketing, sales, support
    is_public: bool = Field(default=True)  # Whether this registration is visible to all
    notes: Optional[str] = Field(default=None, nullable=True)
    photo_url: Optional[str] = Field(default=None, nullable=True)  # Path to uploaded photo
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    action: str = Field(max_length=50)  # create, update, delete, view
    model_name: str = Field(max_length=50)  # products, webinar_registrants, users
    record_id: str = Field(max_length=50)
    changes: Optional[str] = Field(default=None, nullable=True)  # JSON of changes
    ip_address: Optional[str] = Field(default=None, nullable=True)
    user_agent: Optional[str] = Field(default=None, nullable=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))