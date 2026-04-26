"""
Cream & Co. — Order State
===========================
Order placement, cancellation, history, and status tracking.
"""

import reflex as rx
from sqlmodel import select, col
from datetime import datetime
from typing import Any

from ..models.order import Order, OrderItem
from ..models.cart import CartItem
from ..models.product import Product
from ..services.email_service import (
    send_order_confirmation_email,
    send_order_cancelled_email,
    notify_owner_new_order,
    notify_owner_order_cancelled,
)


class OrderState(rx.State):
    """State for managing customer orders."""

    # ── Data ──────────────────────────────────────────────────────────────
    orders: list[dict[str, Any]] = []
    current_order: dict[str, Any] = {}
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""

    # ── Checkout Form ─────────────────────────────────────────────────────
    checkout_address: str = ""
    checkout_phone: str = ""
    checkout_notes: str = ""
    checkout_payment: str = "cod"

    # ── Explicit Setters (Reflex 0.9 compatibility) ───────────────────────
    @rx.event
    def set_checkout_address(self, value: str):
        self.checkout_address = value

    @rx.event
    def set_checkout_phone(self, value: str):
        self.checkout_phone = value

    @rx.event
    def set_checkout_notes(self, value: str):
        self.checkout_notes = value

    @rx.event
    def set_checkout_payment(self, value: str):
        self.checkout_payment = value

    # ─────────────────────────────────────────────────────────────────────
    # Place Order
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    async def place_order(self):
        """Create a new order from the current cart."""
        self.error_message = ""
        self.success_message = ""
        self.is_loading = True

        from .auth_state import AuthState
        from .cart_state import CartState

        auth = await self.get_state(AuthState)
        cart = await self.get_state(CartState)

        if not auth.is_authenticated:
            self.error_message = "Please log in to place an order."
            self.is_loading = False
            return rx.redirect("/login")

        if cart.is_cart_empty:
            self.error_message = "Your cart is empty."
            self.is_loading = False
            return

        if not self.checkout_address.strip():
            self.error_message = "Please enter your delivery address."
            self.is_loading = False
            return

        if not self.checkout_phone.strip():
            self.error_message = "Please enter your phone number."
            self.is_loading = False
            return

        try:
            with rx.session() as session:
                # ── Stock validation ──────────────────────────────────
                for cart_item in cart.cart_items:
                    product = session.exec(
                        select(Product).where(Product.id == cart_item["product_id"])
                    ).first()
                    if product and product.stock_quantity >= 0:
                        if product.stock_quantity < cart_item["quantity"]:
                            self.error_message = (
                                f"'{product.name}' has only {product.stock_quantity} left in stock."
                            )
                            self.is_loading = False
                            return

                order = Order(
                    user_id=auth.user_id,
                    subtotal=cart.subtotal,
                    delivery_fee=cart.delivery_fee,
                    total_amount=cart.total,
                    delivery_address=self.checkout_address.strip(),
                    phone=self.checkout_phone.strip(),
                    payment_method=self.checkout_payment,
                    notes=self.checkout_notes.strip(),
                    status="pending",
                )
                session.add(order)
                session.flush()

                items_parts = []
                for cart_item in cart.cart_items:
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=cart_item["product_id"],
                        quantity=cart_item["quantity"],
                        unit_price=cart_item["price"],
                        total_price=cart_item["price"] * cart_item["quantity"],
                    )
                    session.add(order_item)
                    items_parts.append(
                        f"{cart_item['name']} x{cart_item['quantity']}"
                    )

                    # ── Deduct stock ──────────────────────────────────
                    product = session.exec(
                        select(Product).where(Product.id == cart_item["product_id"])
                    ).first()
                    if product and product.stock_quantity >= 0:
                        product.stock_quantity = max(0, product.stock_quantity - cart_item["quantity"])
                        if product.stock_quantity == 0:
                            product.is_available = False
                        session.add(product)

                session.commit()
                items_text = ", ".join(items_parts)

                # Build structured items for PDF invoice
                invoice_items = [
                    {
                        "name": ci["name"],
                        "quantity": ci["quantity"],
                        "unit_price": ci["price"],
                        "total_price": ci["price"] * ci["quantity"],
                    }
                    for ci in cart.cart_items
                ]

                # Email to customer (with PDF invoice attached)
                try:
                    send_order_confirmation_email(
                        to_email=auth.user_email,
                        full_name=auth.user_name,
                        order_number=order.order_number,
                        total_amount=order.total_amount,
                        items_summary=items_text,
                        items=invoice_items,
                        subtotal=order.subtotal,
                        delivery_fee=order.delivery_fee,
                        delivery_address=self.checkout_address.strip(),
                    )
                except Exception as e:
                    print(f"Customer email failed: {e}")

                # WhatsApp to customer
                try:
                    from ..services.whatsapp_service import send_whatsapp_order_status
                    send_whatsapp_order_status(
                        phone=self.checkout_phone.strip(),
                        order_number=order.order_number,
                        status_message="has been placed and is being prepared!",
                    )
                except Exception as e:
                    print(f"WhatsApp notification failed: {e}")

                # Email to owner
                try:
                    notify_owner_new_order(
                        customer_name=auth.user_name,
                        customer_email=auth.user_email,
                        customer_phone=self.checkout_phone.strip(),
                        order_number=order.order_number,
                        total_amount=order.total_amount,
                        items_summary=items_text,
                        delivery_address=self.checkout_address.strip(),
                        payment_method=self.checkout_payment,
                    )
                except Exception as e:
                    print(f"Owner notification failed: {e}")

                # Clear cart
                cart_items_db = session.exec(
                    select(CartItem).where(CartItem.user_id == auth.user_id)
                ).all()
                for ci in cart_items_db:
                    session.delete(ci)
                session.commit()

                cart.cart_items = []
                cart._sync_quantities()

                self.current_order = {
                    "order_number": order.order_number,
                    "total_amount": order.total_amount,
                    "status": order.status,
                }
                self.success_message = f"Order {order.order_number} placed!"
                self.checkout_address = ""
                self.checkout_phone = ""
                self.checkout_notes = ""
                self.is_loading = False
                return rx.redirect("/account/orders")

        except Exception as e:
            self.error_message = "Failed to place order. Please try again."
            print(f"Place order error: {e}")
            self.is_loading = False

    # ─────────────────────────────────────────────────────────────────────
    # Cancel Order
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    async def cancel_order(self, order_id: int):
        """Cancel a pending order."""
        from .auth_state import AuthState
        auth = await self.get_state(AuthState)

        if not auth.is_authenticated:
            return

        try:
            with rx.session() as session:
                order = session.exec(
                    select(Order).where(
                        Order.id == order_id,
                        Order.user_id == auth.user_id,
                    )
                ).first()

                if not order:
                    self.error_message = "Order not found."
                    return rx.toast.error("Order not found.")

                if order.status not in ("pending", "confirmed"):
                    self.error_message = "This order cannot be cancelled."
                    return rx.toast.error("Order cannot be cancelled at this stage.")

                order.status = "cancelled"
                order.updated_at = datetime.utcnow().isoformat()
                session.add(order)

                # ── Restore stock ─────────────────────────────────
                order_items = session.exec(
                    select(OrderItem).where(OrderItem.order_id == order.id)
                ).all()
                for oi in order_items:
                    product = session.exec(
                        select(Product).where(Product.id == oi.product_id)
                    ).first()
                    if product and product.stock_quantity >= 0:
                        product.stock_quantity += oi.quantity
                        product.is_available = True
                        session.add(product)

                session.commit()

                # Email customer
                try:
                    send_order_cancelled_email(
                        to_email=auth.user_email,
                        full_name=auth.user_name,
                        order_number=order.order_number,
                    )
                except Exception:
                    pass

                # Notify owner
                try:
                    notify_owner_order_cancelled(
                        customer_name=auth.user_name,
                        order_number=order.order_number,
                        total_amount=order.total_amount,
                    )
                except Exception:
                    pass

                await self.load_user_orders()
                return rx.toast.success(f"Order {order.order_number} cancelled.")

        except Exception as e:
            print(f"Cancel order error: {e}")
            return rx.toast.error("Failed to cancel order.")

    # ─────────────────────────────────────────────────────────────────────
    # Load Orders (User)
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    async def load_user_orders(self):
        """Load all orders for the current user."""
        self.is_loading = True

        from .auth_state import AuthState
        auth = await self.get_state(AuthState)

        if not auth.is_authenticated:
            self.orders = []
            self.is_loading = False
            return

        try:
            with rx.session() as session:
                user_orders = session.exec(
                    select(Order)
                    .where(Order.user_id == auth.user_id)
                    .order_by(col(Order.created_at).desc())
                ).all()

                orders_list = []
                for o in user_orders:
                    items = session.exec(
                        select(OrderItem).where(OrderItem.order_id == o.id)
                    ).all()

                    item_parts = []
                    for item in items:
                        product = session.exec(
                            select(Product).where(Product.id == item.product_id)
                        ).first()
                        name = product.name if product else "Unknown"
                        item_parts.append(f"{name} × {item.quantity}")

                    orders_list.append({
                        "id": o.id,
                        "order_number": o.order_number,
                        "total_amount": o.total_amount,
                        "status": o.status,
                        "created_at": o.created_at,
                        "delivery_address": o.delivery_address,
                        "payment_method": o.payment_method,
                        "items_summary": ", ".join(item_parts),
                    })

                self.orders = orders_list

        except Exception as e:
            print(f"Error loading orders: {e}")
        finally:
            self.is_loading = False

    # ─────────────────────────────────────────────────────────────────────
    # Pre-fill Checkout
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    async def prefill_checkout(self):
        """Pre-fill checkout form with user's saved address and phone."""
        from .auth_state import AuthState
        auth = await self.get_state(AuthState)
        if auth.is_authenticated:
            self.checkout_address = auth.user_address
            self.checkout_phone = auth.user_phone
