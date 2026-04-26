"""
Cream & Co. — Order Models
============================
Order management with individual line items and status tracking.
"""

import reflex as rx
from sqlmodel import Field
from typing import Optional
from datetime import datetime
import uuid


class Order(rx.Model, table=True):
    """Customer order with status tracking and delivery details."""

    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_number: str = Field(
        default_factory=lambda: f"CC-{uuid.uuid4().hex[:8].upper()}",
        unique=True,
        index=True,
        max_length=20,
    )
    user_id: str = Field(foreign_key="users.id", max_length=36, index=True)

    # Pricing
    subtotal: float = Field(default=0.0, ge=0)
    delivery_fee: float = Field(default=0.0, ge=0)
    discount: float = Field(default=0.0, ge=0)
    total_amount: float = Field(default=0.0, ge=0)

    # Status: pending → confirmed → preparing → out_for_delivery → delivered / cancelled
    status: str = Field(default="pending", max_length=20)

    # Delivery details
    delivery_address: str = Field(default="", max_length=500)
    phone: str = Field(default="", max_length=15)
    payment_method: str = Field(default="cod", max_length=20)
    notes: str = Field(default="", max_length=500)

    # Timestamps
    created_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        max_length=30,
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        max_length=30,
    )


class OrderItem(rx.Model, table=True):
    """Individual line item within an order."""

    __tablename__ = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", index=True)
    product_id: int = Field(foreign_key="products.id")
    quantity: int = Field(default=1, ge=1)
    unit_price: float = Field(ge=0)
    total_price: float = Field(ge=0)
