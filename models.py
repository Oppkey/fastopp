# =========================
# demo_assets/models.py
# Full models for demo_assets - all models
# =========================
from datetime import UTC, datetime
import uuid

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)  # New field for staff permissions
    group: str | None = Field(default=None)  # marketing, sales, support, etc.


class Product(SQLModel, table=True):
    __tablename__ = "products"  # type: ignore

    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    description: str | None = Field(default=None, nullable=True)
    price: float = Field(nullable=False)
    category: str | None = Field(max_length=50, default=None, nullable=True)
    in_stock: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class WebinarRegistrants(SQLModel, table=True):
    __tablename__ = "webinar_registrants"  # type: ignore

    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    company: str | None = Field(max_length=100, default=None, nullable=True)
    webinar_title: str = Field(max_length=200, nullable=False)
    webinar_date: datetime = Field(nullable=False)
    registration_date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    status: str = Field(default="registered")  # registered, attended, cancelled, no_show
    assigned_sales_rep: str | None = Field(default=None, nullable=True)
    group: str | None = Field(default=None)  # marketing, sales, support
    is_public: bool = Field(default=True)  # Whether this registration is visible to all
    notes: str | None = Field(default=None, nullable=True)
    photo_url: str | None = Field(default=None, nullable=True)  # Path to uploaded photo
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"  # type: ignore

    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    action: str = Field(max_length=50)  # create, update, delete, view
    model_name: str = Field(max_length=50)  # products, webinar_registrants, users
    record_id: str = Field(max_length=50)
    changes: str | None = Field(default=None, nullable=True)  # JSON of changes
    ip_address: str | None = Field(default=None, nullable=True)
    user_agent: str | None = Field(default=None, nullable=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
