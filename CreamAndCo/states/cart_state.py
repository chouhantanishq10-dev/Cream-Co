"""
Cream & Co. — Cart State
==========================
Shopping cart management with persistent storage for authenticated users.
Tracks per-product quantities for inline +/- controls on product cards.
"""

import reflex as rx
from sqlmodel import select
from typing import Any

from ..models.cart import CartItem
from ..models.product import Product
from ..utils.constants import DELIVERY_FEE, FREE_DELIVERY_THRESHOLD


class CartState(rx.State):
    """Shopping cart state with add/remove/update operations."""

    # ── Cart Data ─────────────────────────────────────────────────────────
    cart_items: list[dict[str, Any]] = []
    cart_product_ids: list[int] = []       # product IDs currently in cart
    cart_quantities: dict[str, int] = {}   # "product_id" -> quantity
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""

    # ── Computed Properties ───────────────────────────────────────────────
    @rx.var
    def cart_count(self) -> int:
        return sum(item.get("quantity", 0) for item in self.cart_items)

    @rx.var
    def subtotal(self) -> float:
        return sum(
            item.get("price", 0) * item.get("quantity", 0)
            for item in self.cart_items
        )

    @rx.var
    def delivery_fee(self) -> float:
        if self.subtotal >= FREE_DELIVERY_THRESHOLD or self.subtotal == 0:
            return 0.0
        return DELIVERY_FEE

    @rx.var
    def total(self) -> float:
        return self.subtotal + self.delivery_fee

    @rx.var
    def is_cart_empty(self) -> bool:
        return len(self.cart_items) == 0

    def _sync_quantities(self):
        """Sync cart_product_ids and cart_quantities from cart_items."""
        self.cart_product_ids = [
            item["product_id"] for item in self.cart_items
        ]
        self.cart_quantities = {
            str(item["product_id"]): item["quantity"]
            for item in self.cart_items
        }

    # ─────────────────────────────────────────────────────────────────────
    # Load Cart
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    async def load_cart(self):
        """Load cart items from database for the current user."""
        from .auth_state import AuthState
        auth = await self.get_state(AuthState)
        if not auth.user_id:
            return

        self.is_loading = True
        try:
            with rx.session() as session:
                items = session.exec(
                    select(CartItem).where(CartItem.user_id == auth.user_id)
                ).all()

                cart_list = []
                for item in items:
                    product = session.exec(
                        select(Product).where(Product.id == item.product_id)
                    ).first()
                    if product:
                        unit_price = product.discount_price or product.price
                        cart_list.append({
                            "cart_item_id": item.id,
                            "product_id": product.id,
                            "name": product.name,
                            "price": unit_price,
                            "image_url": product.image_url,
                            "quantity": item.quantity,
                            "line_total": unit_price * item.quantity,
                            "weight_info": product.weight_info,
                            "is_veg": product.is_veg,
                        })
                self.cart_items = cart_list
                self._sync_quantities()
        except Exception as e:
            print(f"Error loading cart: {e}")
        finally:
            self.is_loading = False

    # ─────────────────────────────────────────────────────────────────────
    # Add to Cart (by product_id — used from product cards)
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    async def add_to_cart(self, product_id: int):
        """Add a product to cart (qty 1) or increment if exists."""
        self.error_message = ""
        self.success_message = ""

        from .auth_state import AuthState
        auth = await self.get_state(AuthState)
        if not auth.is_authenticated:
            self.error_message = "Please log in to add items to cart."
            return [
                rx.toast.error("Please log in first"),
                rx.redirect("/login"),
            ]

        try:
            with rx.session() as session:
                existing = session.exec(
                    select(CartItem).where(
                        CartItem.user_id == auth.user_id,
                        CartItem.product_id == product_id,
                    )
                ).first()

                if existing:
                    existing.quantity += 1
                    session.add(existing)
                else:
                    session.add(CartItem(
                        user_id=auth.user_id,
                        product_id=product_id,
                        quantity=1,
                    ))
                session.commit()
                await self.load_cart()
                self.success_message = "Added to cart!"
                return rx.toast.success("Added to cart! 🛒")
        except Exception as e:
            self.error_message = "Failed to add to cart."
            print(f"Add to cart error: {e}")
            return rx.toast.error("Failed to add to cart.")

    # ─────────────────────────────────────────────────────────────────────
    # Decrement by Product ID (used from product cards)
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    async def decrement_product(self, product_id: int):
        """Decrement qty of a product. Remove if qty reaches 0."""
        from .auth_state import AuthState
        auth = await self.get_state(AuthState)
        if not auth.is_authenticated:
            return

        try:
            with rx.session() as session:
                item = session.exec(
                    select(CartItem).where(
                        CartItem.user_id == auth.user_id,
                        CartItem.product_id == product_id,
                    )
                ).first()
                if item:
                    if item.quantity <= 1:
                        session.delete(item)
                    else:
                        item.quantity -= 1
                        session.add(item)
                    session.commit()
                    await self.load_cart()
        except Exception as e:
            print(f"Decrement error: {e}")

    # ─────────────────────────────────────────────────────────────────────
    # Update Quantity (by cart_item_id — used from cart page)
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    async def update_quantity(self, cart_item_id: int, new_quantity: int):
        if new_quantity < 1:
            return self.remove_from_cart(cart_item_id)
        try:
            with rx.session() as session:
                item = session.exec(
                    select(CartItem).where(CartItem.id == cart_item_id)
                ).first()
                if item:
                    item.quantity = new_quantity
                    session.add(item)
                    session.commit()
                    await self.load_cart()
        except Exception as e:
            print(f"Update quantity error: {e}")

    @rx.event
    async def increment_item(self, cart_item_id: int):
        for item in self.cart_items:
            if item.get("cart_item_id") == cart_item_id:
                await self.update_quantity(cart_item_id, item["quantity"] + 1)
                return

    @rx.event
    async def decrement_item(self, cart_item_id: int):
        for item in self.cart_items:
            if item.get("cart_item_id") == cart_item_id:
                await self.update_quantity(cart_item_id, item["quantity"] - 1)
                return

    # ─────────────────────────────────────────────────────────────────────
    # Remove / Clear
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    async def remove_from_cart(self, cart_item_id: int):
        try:
            with rx.session() as session:
                item = session.exec(
                    select(CartItem).where(CartItem.id == cart_item_id)
                ).first()
                if item:
                    session.delete(item)
                    session.commit()
                    await self.load_cart()
        except Exception as e:
            print(f"Remove from cart error: {e}")

    @rx.event
    async def clear_cart(self):
        from .auth_state import AuthState
        auth = await self.get_state(AuthState)
        if not auth.user_id:
            return
        try:
            with rx.session() as session:
                items = session.exec(
                    select(CartItem).where(CartItem.user_id == auth.user_id)
                ).all()
                for item in items:
                    session.delete(item)
                session.commit()
                self.cart_items = []
                self._sync_quantities()
        except Exception as e:
            print(f"Clear cart error: {e}")
