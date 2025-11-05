# =========================
# base_assets/models.py
# Minimal models for base_assets - only User model
# =========================
from typing import Optional
import uuid

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_staff: bool = Field(default=False)  # New field for staff permissions
    group: Optional[str] = Field(default=None)  # marketing, sales, support, etc.
