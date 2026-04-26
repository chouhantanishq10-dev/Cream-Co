"""
Cream & Co. — Admin State
===========================
Admin dashboard with product, order, and user management.
"""

import reflex as rx
from sqlmodel import select, col, func
from datetime import datetime
from typing import Any

from ..models.user import User
from ..models.product import Product, Category
from ..models.order import Order, OrderItem


class AdminState(rx.State):
    """Admin panel state for managing the bakery operations."""

    # ── Dashboard Stats ───────────────────────────────────────────────────
    total_orders: int = 0
    total_revenue: float = 0.0
    total_users: int = 0
    total_products: int = 0
    pending_orders: int = 0

    # ── Analytics ─────────────────────────────────────────────────────────
    today_revenue: float = 0.0
    today_orders: int = 0
    daily_revenue: list[dict[str, Any]] = []    # [{date, revenue, orders}]
    monthly_revenue: list[dict[str, Any]] = []  # [{month, revenue, orders}]
    best_sellers: list[dict[str, Any]] = []     # [{name, qty_sold, revenue}]
    low_stock_products: list[dict[str, Any]] = []  # [{name, stock}]
    order_status_counts: dict[str, int] = {}    # {pending: 2, delivered: 5}

    # ── Data Lists ────────────────────────────────────────────────────────
    all_orders: list[dict[str, Any]] = []
    all_users: list[dict[str, Any]] = []
    all_products: list[dict[str, Any]] = []

    # ── UI State ──────────────────────────────────────────────────────────
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""

    # ── Product Form ──────────────────────────────────────────────────────
    edit_product_id: int = 0
    form_name: str = ""
    form_description: str = ""
    form_price: str = ""
    form_image_url: str = ""
    form_category_id: str = ""
    form_weight_info: str = ""
    form_stock: str = "-1"
    form_is_veg: bool = True
    form_is_bestseller: bool = False
    form_is_available: bool = True
    show_product_modal: bool = False

    # ── Explicit Setters (Reflex 0.9 compatibility) ───────────────────────
    @rx.event
    def set_form_name(self, value: str):
        self.form_name = value

    @rx.event
    def set_form_description(self, value: str):
        self.form_description = value

    @rx.event
    def set_form_price(self, value: str):
        self.form_price = value

    @rx.event
    def set_form_image_url(self, value: str):
        self.form_image_url = value

    @rx.event
    def set_form_category_id(self, value: str):
        self.form_category_id = value

    @rx.event
    def set_form_weight_info(self, value: str):
        self.form_weight_info = value

    @rx.event
    def set_form_stock(self, value: str):
        self.form_stock = value

    # ─────────────────────────────────────────────────────────────────────
    # Dashboard
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def load_dashboard(self):
        """Load dashboard statistics."""
        self.is_loading = True
        try:
            with rx.session() as session:
                self.total_orders = len(session.exec(select(Order)).all())
                self.total_users = len(session.exec(select(User)).all())
                self.total_products = len(session.exec(select(Product)).all())

                # Calculate revenue from delivered orders
                delivered = session.exec(
                    select(Order).where(Order.status == "delivered")
                ).all()
                self.total_revenue = sum(o.total_amount for o in delivered)

                # Pending orders count
                pending = session.exec(
                    select(Order).where(Order.status == "pending")
                ).all()
                self.pending_orders = len(pending)

                # ── Analytics ─────────────────────────────────────
                all_orders = session.exec(select(Order)).all()

                # Today's stats
                today_str = datetime.utcnow().strftime("%Y-%m-%d")
                today_delivered = [
                    o for o in all_orders
                    if o.created_at[:10] == today_str
                    and o.status not in ("cancelled",)
                ]
                self.today_orders = len(today_delivered)
                self.today_revenue = sum(o.total_amount for o in today_delivered)

                # Order status breakdown
                status_map: dict[str, int] = {}
                for o in all_orders:
                    status_map[o.status] = status_map.get(o.status, 0) + 1
                self.order_status_counts = status_map

                # Daily revenue (last 30 days)
                from collections import defaultdict
                daily: dict[str, dict] = defaultdict(lambda: {"revenue": 0.0, "orders": 0})
                for o in all_orders:
                    if o.status != "cancelled":
                        day = o.created_at[:10]
                        daily[day]["revenue"] += o.total_amount
                        daily[day]["orders"] += 1
                sorted_days = sorted(daily.keys(), reverse=True)[:30]
                max_rev = max((daily[d]["revenue"] for d in sorted_days), default=1) or 1
                self.daily_revenue = [
                    {
                        "date": d,
                        "revenue": round(daily[d]["revenue"], 2),
                        "orders": daily[d]["orders"],
                        "bar_width": f"{int(daily[d]['revenue'] / max_rev * 200)}px",
                    }
                    for d in reversed(sorted_days)
                ]

                # Monthly revenue (last 12 months)
                monthly: dict[str, dict] = defaultdict(lambda: {"revenue": 0.0, "orders": 0})
                for o in all_orders:
                    if o.status != "cancelled":
                        month_key = o.created_at[:7]  # YYYY-MM
                        monthly[month_key]["revenue"] += o.total_amount
                        monthly[month_key]["orders"] += 1
                sorted_months = sorted(monthly.keys(), reverse=True)[:12]
                self.monthly_revenue = [
                    {"month": m, "revenue": round(monthly[m]["revenue"], 2), "orders": monthly[m]["orders"]}
                    for m in reversed(sorted_months)
                ]

                # Best sellers (by quantity sold)
                items = session.exec(select(OrderItem)).all()
                product_sales: dict[int, dict] = defaultdict(lambda: {"qty": 0, "revenue": 0.0})
                for item in items:
                    product_sales[item.product_id]["qty"] += item.quantity
                    product_sales[item.product_id]["revenue"] += item.total_price
                top_ids = sorted(product_sales, key=lambda pid: product_sales[pid]["qty"], reverse=True)[:10]
                sellers = []
                for pid in top_ids:
                    prod = session.exec(select(Product).where(Product.id == pid)).first()
                    if prod:
                        sellers.append({
                            "name": prod.name,
                            "qty_sold": product_sales[pid]["qty"],
                            "revenue": round(product_sales[pid]["revenue"], 2),
                        })
                self.best_sellers = sellers

                # Low stock alerts
                low_stock = session.exec(
                    select(Product).where(
                        Product.stock_quantity >= 0,
                        Product.stock_quantity <= 10,
                    )
                ).all()
                self.low_stock_products = [
                    {"name": p.name, "stock": p.stock_quantity}
                    for p in low_stock
                ]

        except Exception as e:
            print(f"Dashboard load error: {e}")
        finally:
            self.is_loading = False

    # ─────────────────────────────────────────────────────────────────────
    # Order Management
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def load_all_orders(self):
        """Load all orders for admin view."""
        self.is_loading = True
        try:
            with rx.session() as session:
                orders = session.exec(
                    select(Order).order_by(col(Order.created_at).desc())
                ).all()

                order_list = []
                for o in orders:
                    # Get user info
                    user = session.exec(
                        select(User).where(User.id == o.user_id)
                    ).first()

                    # Get item count
                    items = session.exec(
                        select(OrderItem).where(OrderItem.order_id == o.id)
                    ).all()

                    order_list.append(
                        {
                            "id": o.id,
                            "order_number": o.order_number,
                            "customer_name": user.full_name if user else "Unknown",
                            "customer_email": user.email if user else "",
                            "customer_phone": o.phone,
                            "total_amount": o.total_amount,
                            "status": o.status,
                            "payment_method": o.payment_method,
                            "delivery_address": o.delivery_address,
                            "notes": o.notes,
                            "item_count": len(items),
                            "created_at": o.created_at,
                        }
                    )

                self.all_orders = order_list

        except Exception as e:
            print(f"Error loading orders: {e}")
        finally:
            self.is_loading = False

    @rx.event
    def update_order_status(self, order_id: int, new_status: str):
        """Update the status of an order and notify customer."""
        self.error_message = ""
        try:
            with rx.session() as session:
                order = session.exec(
                    select(Order).where(Order.id == order_id)
                ).first()
                if order:
                    old_status = order.status
                    order.status = new_status
                    order.updated_at = datetime.utcnow().isoformat()
                    session.add(order)
                    session.commit()

                    # Send status update email to customer
                    if old_status != new_status:
                        try:
                            user = session.exec(
                                select(User).where(User.id == order.user_id)
                            ).first()
                            if user:
                                from ..services.email_service import send_order_status_email
                                send_order_status_email(
                                    to_email=user.email,
                                    full_name=user.full_name,
                                    order_number=order.order_number,
                                    new_status=new_status,
                                )

                                # WhatsApp notification
                                if user.phone:
                                    try:
                                        from ..services.whatsapp_service import send_whatsapp_order_status
                                        status_messages = {
                                            "confirmed": "has been confirmed!",
                                            "preparing": "is being prepared by our team.",
                                            "out_for_delivery": "is out for delivery!",
                                            "delivered": "has been delivered. Enjoy!",
                                            "cancelled": "has been cancelled.",
                                        }
                                        send_whatsapp_order_status(
                                            phone=user.phone,
                                            order_number=order.order_number,
                                            status_message=status_messages.get(
                                                new_status, f"status: {new_status}"
                                            ),
                                        )
                                    except Exception as e:
                                        print(f"WhatsApp status failed: {e}")
                        except Exception as e:
                            print(f"Status email failed: {e}")

                    self.success_message = f"Order {order.order_number} → {new_status.replace('_', ' ').title()}"
                    self.load_all_orders()
        except Exception as e:
            self.error_message = f"Failed to update order status."
            print(f"Update order error: {e}")

    # ─────────────────────────────────────────────────────────────────────
    # Product Management
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def load_all_products(self):
        """Load all products for admin management."""
        self.is_loading = True
        try:
            with rx.session() as session:
                products = session.exec(select(Product)).all()
                self.all_products = [
                    {
                        "id": p.id,
                        "name": p.name,
                        "slug": p.slug,
                        "price": p.price,
                        "category_id": p.category_id,
                        "is_veg": p.is_veg,
                        "is_bestseller": p.is_bestseller,
                        "is_available": p.is_available,
                        "weight_info": p.weight_info,
                        "stock_quantity": p.stock_quantity,
                        "is_low_stock": 0 < p.stock_quantity <= 10,
                        "is_unlimited": p.stock_quantity < 0,
                    }
                    for p in products
                ]
        except Exception as e:
            print(f"Error loading products: {e}")
        finally:
            self.is_loading = False

    @rx.event
    def toggle_product_availability(self, product_id: int):
        """Toggle product availability on/off."""
        try:
            with rx.session() as session:
                product = session.exec(
                    select(Product).where(Product.id == product_id)
                ).first()
                if product:
                    product.is_available = not product.is_available
                    product.updated_at = datetime.utcnow().isoformat()
                    session.add(product)
                    session.commit()
                    self.load_all_products()
        except Exception as e:
            print(f"Toggle availability error: {e}")

    @rx.event
    def open_product_modal(self, product_id: int = 0):
        """Open product edit/add modal."""
        self.edit_product_id = product_id
        if product_id > 0:
            # Edit mode — load product data
            try:
                with rx.session() as session:
                    p = session.exec(
                        select(Product).where(Product.id == product_id)
                    ).first()
                    if p:
                        self.form_name = p.name
                        self.form_description = p.description
                        self.form_price = str(p.price)
                        self.form_image_url = p.image_url or ""
                        self.form_category_id = str(p.category_id)
                        self.form_weight_info = p.weight_info
                        self.form_stock = str(p.stock_quantity)
                        self.form_is_veg = p.is_veg
                        self.form_is_bestseller = p.is_bestseller
                        self.form_is_available = p.is_available
            except Exception as e:
                print(f"Load product error: {e}")
        else:
            # Add mode — clear form
            self.form_name = ""
            self.form_description = ""
            self.form_price = ""
            self.form_image_url = ""
            self.form_category_id = "1"
            self.form_weight_info = ""
            self.form_stock = "-1"
            self.form_is_veg = True
            self.form_is_bestseller = False
            self.form_is_available = True

        self.show_product_modal = True

    @rx.event
    def close_product_modal(self):
        """Close the product modal."""
        self.show_product_modal = False

    @rx.event
    def save_product(self):
        """Save (create or update) a product."""
        self.error_message = ""
        from slugify import slugify

        if not self.form_name.strip():
            self.error_message = "Product name is required."
            return

        try:
            price = float(self.form_price)
        except (ValueError, TypeError):
            self.error_message = "Please enter a valid price."
            return

        try:
            with rx.session() as session:
                if self.edit_product_id > 0:
                    # Update existing
                    product = session.exec(
                        select(Product).where(
                            Product.id == self.edit_product_id
                        )
                    ).first()
                    if product:
                        product.name = self.form_name.strip()
                        product.slug = slugify(self.form_name.strip())
                        product.description = self.form_description.strip()
                        product.price = price
                        product.image_url = self.form_image_url.strip()
                        product.category_id = int(self.form_category_id)
                        product.weight_info = self.form_weight_info.strip()
                        product.stock_quantity = int(self.form_stock) if self.form_stock.strip() else -1
                        product.is_veg = self.form_is_veg
                        product.is_bestseller = self.form_is_bestseller
                        product.is_available = self.form_is_available
                        product.updated_at = datetime.utcnow().isoformat()
                        session.add(product)
                else:
                    # Create new
                    product = Product(
                        name=self.form_name.strip(),
                        slug=slugify(self.form_name.strip()),
                        description=self.form_description.strip(),
                        price=price,
                        image_url=self.form_image_url.strip(),
                        category_id=int(self.form_category_id),
                        weight_info=self.form_weight_info.strip(),
                        stock_quantity=int(self.form_stock) if self.form_stock.strip() else -1,
                        is_veg=self.form_is_veg,
                        is_bestseller=self.form_is_bestseller,
                        is_available=self.form_is_available,
                    )
                    session.add(product)

                session.commit()
                self.success_message = "Product saved successfully!"
                self.show_product_modal = False
                self.load_all_products()

        except Exception as e:
            self.error_message = "Failed to save product."
            print(f"Save product error: {e}")

    # ─────────────────────────────────────────────────────────────────────
    # User Management
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def load_all_users(self):
        """Load all users for admin management."""
        self.is_loading = True
        try:
            with rx.session() as session:
                users = session.exec(
                    select(User).order_by(col(User.created_at).desc())
                ).all()
                self.all_users = [
                    {
                        "id": u.id,
                        "email": u.email,
                        "full_name": u.full_name,
                        "phone": u.phone,
                        "is_verified": u.is_verified,
                        "is_admin": u.is_admin,
                        "created_at": u.created_at,
                    }
                    for u in users
                ]
        except Exception as e:
            print(f"Error loading users: {e}")
        finally:
            self.is_loading = False

    @rx.event
    def toggle_user_admin(self, user_id: str):
        """Toggle admin status for a user."""
        try:
            with rx.session() as session:
                user = session.exec(
                    select(User).where(User.id == user_id)
                ).first()
                if user:
                    user.is_admin = not user.is_admin
                    user.updated_at = datetime.utcnow().isoformat()
                    session.add(user)
                    session.commit()
                    self.load_all_users()
        except Exception as e:
            print(f"Toggle admin error: {e}")
