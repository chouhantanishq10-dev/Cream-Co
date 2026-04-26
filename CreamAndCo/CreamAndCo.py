"""
Cream & Co. — Main Application Entry Point
=============================================
Registers all routes, imports all models for database migration,
and configures the Reflex application.
"""

import reflex as rx

# ── Import all models so Reflex creates database tables ──────────────────
from .models.user import User
from .models.product import Product, Category
from .models.cart import CartItem
from .models.order import Order, OrderItem

# ── Import all pages ─────────────────────────────────────────────────────
from .pages.index import index
from .pages.menu import menu_page
from .pages.auth import (
    login_page,
    register_page,
    verify_email_page,
    forgot_password_page,
    reset_password_page,
)
from .pages.cart import cart_page, checkout_page
from .pages.account import profile_page, orders_page
from .pages.admin import (
    admin_dashboard,
    admin_orders_page,
    admin_products_page,
    admin_users_page,
)
from .pages.static import about_page, contact_page


# ── Global Styles ────────────────────────────────────────────────────────
style = {
    "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "::selection": {
        "background": "#D4A373",
        "color": "white",
    },
}

# ── Application ──────────────────────────────────────────────────────────
app = rx.App(
    style=style,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap",
    ],
)

# ── Route Registration ───────────────────────────────────────────────────
# Public routes
app.add_page(index, route="/", title="Cream & Co. | Fresh Bakery in Dewas")
app.add_page(menu_page, route="/menu", title="Menu | Cream & Co.")
app.add_page(about_page, route="/about", title="About Us | Cream & Co.")
app.add_page(contact_page, route="/contact", title="Contact Us | Cream & Co.")

# Auth routes
app.add_page(login_page, route="/login", title="Login | Cream & Co.")
app.add_page(register_page, route="/register", title="Sign Up | Cream & Co.")
app.add_page(
    verify_email_page, route="/verify", title="Verify Email | Cream & Co."
)
app.add_page(
    forgot_password_page,
    route="/forgot-password",
    title="Forgot Password | Cream & Co.",
)
app.add_page(
    reset_password_page,
    route="/reset-password",
    title="Reset Password | Cream & Co.",
)

# Shopping routes
app.add_page(cart_page, route="/cart", title="Your Cart | Cream & Co.")
app.add_page(checkout_page, route="/checkout", title="Checkout | Cream & Co.")

# Account routes (protected by state logic)
app.add_page(
    profile_page, route="/account/profile", title="My Profile | Cream & Co."
)
app.add_page(
    orders_page, route="/account/orders", title="My Orders | Cream & Co."
)

# Admin routes (protected by state logic)
app.add_page(
    admin_dashboard, route="/admin", title="Admin Dashboard | Cream & Co."
)
app.add_page(
    admin_products_page,
    route="/admin/products",
    title="Manage Products | Cream & Co.",
)
app.add_page(
    admin_orders_page,
    route="/admin/orders",
    title="Manage Orders | Cream & Co.",
)
app.add_page(
    admin_users_page,
    route="/admin/users",
    title="Manage Users | Cream & Co.",
)
