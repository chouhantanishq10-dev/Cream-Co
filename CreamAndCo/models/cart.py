"""
Cream & Co. — Cart Model
=========================
Shopping cart items linked to authenticated users.
"""

import reflex as rx
from sqlmodel import Field
from typing import Optional
from datetime import datetime


class CartItem(rx.Model, table=True):
    """Shopping cart item linking a user to a product with quantity."""

    __tablename__ = "cart_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", max_length=36, index=True)
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field(default=1, ge=1)
    added_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        max_length=30,
    )
