"""
Cream & Co. — Product & Category Models
========================================
Product catalog with categories for the bakery menu.
"""

import reflex as rx
from sqlmodel import Field
from typing import Optional
from datetime import datetime


class Category(rx.Model, table=True):
    """Product category (e.g., Specials, Combos, Cakes, Tub Cakes)."""

    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    slug: str = Field(max_length=100, unique=True, index=True)
    description: str = Field(default="", max_length=500)
    image_url: str = Field(default="", max_length=500)
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)


class Product(rx.Model, table=True):
    """Individual bakery product with pricing and metadata."""

    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    slug: str = Field(max_length=200, unique=True, index=True)
    description: str = Field(default="", max_length=1000)
    price: float = Field(ge=0)
    discount_price: Optional[float] = Field(default=None)
    image_url: str = Field(default="", max_length=500)
    category_id: int = Field(foreign_key="categories.id")

    # Product attributes
    is_veg: bool = Field(default=True)
    is_bestseller: bool = Field(default=False)
    is_available: bool = Field(default=True)
    weight_info: str = Field(default="", max_length=100)

    # Inventory (-1 = unlimited, 0+ = tracked stock)
    stock_quantity: int = Field(default=-1)

    # Timestamps
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        max_length=30,
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        max_length=30,
    )
