"""
Cream & Co. — User Model
=========================
Handles user accounts, authentication state, and profile data.
"""

import reflex as rx
from sqlmodel import Field
from typing import Optional
from datetime import datetime
import uuid


class User(rx.Model, table=True):
    """User account model for authentication and profile management."""

    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        max_length=36,
    )
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
    )
    password_hash: str = Field(max_length=255)
    full_name: str = Field(max_length=100)
    phone: str = Field(default="", max_length=15)
    address: str = Field(default="", max_length=500)

    # Authentication flags
    is_verified: bool = Field(default=False)
    is_admin: bool = Field(default=False)

    # Email verification
    verification_token: Optional[str] = Field(default=None, max_length=255)
    token_expires_at: Optional[str] = Field(default=None, max_length=30)

    # Password reset
    reset_token: Optional[str] = Field(default=None, max_length=255)
    reset_token_expires: Optional[str] = Field(default=None, max_length=30)

    # Timestamps
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        max_length=30,
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        max_length=30,
    )
