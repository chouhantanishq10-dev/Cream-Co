"""
Cream & Co. — Admin Pages
===========================
Dashboard, product management, order management, user management.
"""

import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..states.admin_state import AdminState
from ..states.auth_state import AuthState


def _admin_guard(*children) -> rx.Component:
    """Guard wrapper — only show content if user is admin."""
    return rx.cond(
        AuthState.is_admin,
        rx.fragment(*children),
        rx.center(
            rx.vstack(
                rx.text("🔒", font_size="48px"),
                rx.heading("Access Denied", size="5", color="#2B2B2B"),
                rx.text("You need admin privileges to access this page.", color="#9CA3AF"),
                rx.link(
                    rx.button("Go Home", bg="#D4A373", color="white", border_radius="10px", cursor="pointer"),
                    href="/",
                ),
                spacing="4",
                align_items="center",
                padding_y="64px",
            ),
        ),
    )


def _stat_card(title: str, value, icon: str, color: str) -> rx.Component:
    """Dashboard stat card."""
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(title, font_size="13px", color="#9CA3AF", font_weight="500"),
                rx.text(
                    value,
                    font_size="28px",
                    font_weight="700",
                    color="#2B2B2B",
                ),
                spacing="1",
                align_items="flex-start",
            ),
            rx.spacer(),
            rx.center(
                rx.icon(icon, size=24, color="white"),
                width="48px",
                height="48px",
                bg=color,
                border_radius="12px",
            ),
            width="100%",
            align_items="center",
        ),
        bg="white",
        border_radius="16px",
        padding="20px",
        box_shadow="0 2px 12px rgba(0,0,0,0.04)",
        width="100%",
    )


# =========================================================================
# Admin Dashboard
# =========================================================================
def admin_dashboard() -> rx.Component:
    """Admin dashboard with key statistics."""
    return rx.box(
        navbar(),
        rx.box(
            _admin_guard(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            "Admin Dashboard",
                            size="6",
                            color="#2B2B2B",
                            font_family="'Playfair Display', serif",
                        ),
                        rx.spacer(),
                        rx.hstack(
                            rx.link(
                                rx.button(
                                    rx.icon("package", size=14),
                                    "Products",
                                    variant="outline",
                                    color="#D4A373",
                                    border_color="#D4A373",
                                    border_radius="10px",
                                    cursor="pointer",
                                    size="2",
                                ),
                                href="/admin/products",
                            ),
                            rx.link(
                                rx.button(
                                    rx.icon("clipboard-list", size=14),
                                    "Orders",
                                    variant="outline",
                                    color="#D4A373",
                                    border_color="#D4A373",
                                    border_radius="10px",
                                    cursor="pointer",
                                    size="2",
                                ),
                                href="/admin/orders",
                            ),
                            rx.link(
                                rx.button(
                                    rx.icon("users", size=14),
                                    "Users",
                                    variant="outline",
                                    color="#D4A373",
                                    border_color="#D4A373",
                                    border_radius="10px",
                                    cursor="pointer",
                                    size="2",
                                ),
                                href="/admin/users",
                            ),
                            spacing="2",
                        ),
                        width="100%",
                        align_items="center",
                        flex_wrap="wrap",
                        gap="12px",
                    ),
                    # Stats grid
                    rx.grid(
                        _stat_card("Total Orders", AdminState.total_orders, "shopping-bag", "#3B82F6"),
                        _stat_card(
                            "Revenue",
                            AdminState.total_revenue,
                            "banknote",
                            "#10B981",
                        ),
                        _stat_card("Total Users", AdminState.total_users, "users", "#8B5CF6"),
                        _stat_card("Products", AdminState.total_products, "cake-slice", "#F59E0B"),
                        columns=rx.breakpoints(initial="1", sm="2", md="4"),
                        spacing="4",
                        width="100%",
                    ),
                    # Pending orders alert
                    rx.cond(
                        AdminState.pending_orders > 0,
                        rx.box(
                            rx.hstack(
                                rx.icon("triangle-alert", size=18, color="#F59E0B"),
                                rx.text(
                                    f"{AdminState.pending_orders} pending order(s) need attention",
                                    font_weight="500",
                                    color="#92400E",
                                    font_size="14px",
                                ),
                                rx.spacer(),
                                rx.link(
                                    rx.button(
                                        "View Orders",
                                        size="1",
                                        bg="#F59E0B",
                                        color="white",
                                        border_radius="8px",
                                        cursor="pointer",
                                    ),
                                    href="/admin/orders",
                                ),
                                spacing="3",
                                width="100%",
                                align_items="center",
                            ),
                            bg="#FFFBEB",
                            border="1px solid #FDE68A",
                            border_radius="12px",
                            padding="16px",
                            width="100%",
                        ),
                    ),
                    # ── Low Stock Alerts ──────────────────────────────
                    rx.cond(
                        AdminState.low_stock_products.length() > 0,
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("package-x", size=18, color="#EF4444"),
                                    rx.text("Low Stock Alerts", font_weight="600", font_size="14px", color="#991B1B"),
                                    spacing="2",
                                    align_items="center",
                                ),
                                rx.foreach(
                                    AdminState.low_stock_products,
                                    lambda p: rx.hstack(
                                        rx.text(p["name"], font_size="13px", color="#6B7280"),
                                        rx.spacer(),
                                        rx.box(
                                            rx.text(
                                                rx.cond(p["stock"] == 0, "SOLD OUT", f"{p['stock']} left"),
                                                font_size="11px",
                                                font_weight="700",
                                                color=rx.cond(p["stock"] == 0, "#EF4444", "#F59E0B"),
                                            ),
                                            bg=rx.cond(p["stock"] == 0, "#FEE2E2", "#FEF3C7"),
                                            padding_x="8px",
                                            padding_y="2px",
                                            border_radius="8px",
                                        ),
                                        width="100%",
                                    ),
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            bg="#FEF2F2",
                            border="1px solid #FECACA",
                            border_radius="12px",
                            padding="16px",
                            width="100%",
                        ),
                    ),
                    # ── Today's Stats ─────────────────────────────────
                    rx.grid(
                        _stat_card("Today's Orders", AdminState.today_orders, "calendar", "#3B82F6"),
                        _stat_card("Today's Revenue", AdminState.today_revenue, "trending-up", "#10B981"),
                        columns=rx.breakpoints(initial="1", sm="2"),
                        spacing="4",
                        width="100%",
                    ),
                    # ── Best Sellers ──────────────────────────────────
                    rx.cond(
                        AdminState.best_sellers.length() > 0,
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("trophy", size=18, color="#F59E0B"),
                                    rx.text("Best Sellers", font_weight="700", font_size="16px", color="#2B2B2B"),
                                    spacing="2",
                                    align_items="center",
                                ),
                                rx.foreach(
                                    AdminState.best_sellers,
                                    lambda item: rx.hstack(
                                        rx.text(item["name"], font_weight="500", font_size="14px", color="#2B2B2B"),
                                        rx.spacer(),
                                        rx.hstack(
                                            rx.box(
                                                rx.text(
                                                    f"{item['qty_sold']} sold",
                                                    font_size="11px",
                                                    font_weight="600",
                                                    color="#7C3AED",
                                                ),
                                                bg="#EDE9FE",
                                                padding_x="8px",
                                                padding_y="2px",
                                                border_radius="8px",
                                            ),
                                            rx.text(
                                                f"₹{item['revenue']}",
                                                font_size="13px",
                                                font_weight="600",
                                                color="#10B981",
                                            ),
                                            spacing="2",
                                        ),
                                        width="100%",
                                        padding_y="6px",
                                        border_bottom="1px solid #F3F4F6",
                                    ),
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            bg="white",
                            border_radius="16px",
                            padding="24px",
                            box_shadow="0 2px 12px rgba(0,0,0,0.04)",
                            width="100%",
                        ),
                    ),
                    # ── Daily Revenue Table ───────────────────────────
                    rx.cond(
                        AdminState.daily_revenue.length() > 0,
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon("bar-chart-3", size=18, color="#3B82F6"),
                                    rx.text("Daily Revenue (Last 30 Days)", font_weight="700", font_size="16px", color="#2B2B2B"),
                                    spacing="2",
                                    align_items="center",
                                ),
                                rx.foreach(
                                    AdminState.daily_revenue,
                                    lambda row: rx.hstack(
                                        rx.text(row["date"], font_size="13px", color="#6B7280", min_width="100px"),
                                        rx.box(
                                            width=row["bar_width"],
                                            max_width="200px",
                                            height="16px",
                                            bg="linear-gradient(90deg, #D4A373, #B8864A)",
                                            border_radius="4px",
                                        ),
                                        rx.text(f"₹{row['revenue']}", font_size="13px", font_weight="600", color="#2B2B2B", min_width="80px", text_align="right"),
                                        rx.text(f"{row['orders']} orders", font_size="11px", color="#9CA3AF", min_width="70px", text_align="right"),
                                        width="100%",
                                        align_items="center",
                                        spacing="2",
                                    ),
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            bg="white",
                            border_radius="16px",
                            padding="24px",
                            box_shadow="0 2px 12px rgba(0,0,0,0.04)",
                            width="100%",
                            overflow_x="auto",
                        ),
                    ),
                    spacing="6",
                    max_width="1200px",
                    margin_x="auto",
                    padding_x="24px",
                    padding_y="32px",
                    width="100%",
                ),
            ),
            bg="#FEFAE0",
            width="100%",
            min_height="60vh",
        ),
        footer(),
        width="100%",
        min_height="100vh",
        bg="#FEFAE0",
        on_mount=AdminState.load_dashboard,
    )


# =========================================================================
# Admin Orders Page
# =========================================================================
def admin_orders_page() -> rx.Component:
    """Admin order management page."""
    return rx.box(
        navbar(),
        rx.box(
            _admin_guard(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            "Manage Orders",
                            size="6",
                            color="#2B2B2B",
                            font_family="'Playfair Display', serif",
                        ),
                        rx.spacer(),
                        rx.link(
                            rx.button(
                                rx.icon("arrow-left", size=14),
                                "Dashboard",
                                variant="ghost",
                                color="#D4A373",
                                cursor="pointer",
                                size="2",
                            ),
                            href="/admin",
                        ),
                        width="100%",
                        align_items="center",
                    ),
                    rx.cond(
                        AdminState.all_orders.length() > 0,
                        rx.vstack(
                            rx.foreach(
                                AdminState.all_orders,
                                lambda order: rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.vstack(
                                                rx.hstack(
                                                    rx.text(
                                                        order["order_number"],
                                                        font_weight="700",
                                                        font_size="15px",
                                                    ),
                                                    rx.box(
                                                        rx.text(
                                                            order["status"],
                                                            font_size="11px",
                                                            font_weight="600",
                                                            text_transform="capitalize",
                                                        ),
                                                        padding_x="8px",
                                                        padding_y="2px",
                                                        border_radius="12px",
                                                        bg=rx.match(
                                                            order["status"],
                                                            ("pending", "#FEF3C7"),
                                                            ("confirmed", "#DBEAFE"),
                                                            ("preparing", "#EDE9FE"),
                                                            ("delivered", "#D1FAE5"),
                                                            ("cancelled", "#FEE2E2"),
                                                            "#F3F4F6",
                                                        ),
                                                        color=rx.match(
                                                            order["status"],
                                                            ("pending", "#D97706"),
                                                            ("confirmed", "#2563EB"),
                                                            ("preparing", "#7C3AED"),
                                                            ("delivered", "#059669"),
                                                            ("cancelled", "#DC2626"),
                                                            "#6B7280",
                                                        ),
                                                    ),
                                                    spacing="2",
                                                    align_items="center",
                                                ),
                                                rx.text(
                                                    f"{order['customer_name']} • {order['customer_phone']}",
                                                    font_size="13px",
                                                    color="#6B7280",
                                                ),
                                                spacing="1",
                                            ),
                                            rx.spacer(),
                                            rx.text(
                                                order['total_amount'],
                                                font_weight="700",
                                                color="#D4A373",
                                                font_size="16px",
                                            ),
                                            width="100%",
                                            align_items="flex-start",
                                        ),
                                        rx.hstack(
                                            rx.text(
                                                order['payment_method'],
                                                font_size="12px",
                                                color="#9CA3AF",
                                            ),
                                            rx.spacer(),
                                            # Status update buttons
                                            rx.select(
                                                ["pending", "confirmed", "preparing", "out_for_delivery", "delivered", "cancelled"],
                                                value=order["status"],
                                                on_change=lambda val: AdminState.update_order_status(order["id"], val),
                                                size="1",
                                                border_radius="8px",
                                            ),
                                            width="100%",
                                            align_items="center",
                                        ),
                                        spacing="3",
                                    ),
                                    bg="white",
                                    border_radius="12px",
                                    padding="16px",
                                    box_shadow="0 1px 4px rgba(0,0,0,0.04)",
                                    width="100%",
                                ),
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        rx.center(
                            rx.text("No orders yet.", color="#9CA3AF", padding_y="48px"),
                        ),
                    ),
                    spacing="6",
                    max_width="900px",
                    margin_x="auto",
                    padding_x="24px",
                    padding_y="32px",
                    width="100%",
                ),
            ),
            bg="#FEFAE0",
            width="100%",
            min_height="60vh",
        ),
        footer(),
        width="100%",
        min_height="100vh",
        bg="#FEFAE0",
        on_mount=AdminState.load_all_orders,
    )


# =========================================================================
# Admin Products Page
# =========================================================================
def admin_products_page() -> rx.Component:
    """Admin product management page."""
    return rx.box(
        navbar(),
        rx.box(
            _admin_guard(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            "Manage Products",
                            size="6",
                            color="#2B2B2B",
                            font_family="'Playfair Display', serif",
                        ),
                        rx.spacer(),
                        rx.hstack(
                            rx.link(
                                rx.button(
                                    rx.icon("arrow-left", size=14),
                                    "Dashboard",
                                    variant="ghost",
                                    color="#D4A373",
                                    cursor="pointer",
                                    size="2",
                                ),
                                href="/admin",
                            ),
                            rx.button(
                                rx.icon("plus", size=14),
                                "Add Product",
                                bg="#D4A373",
                                color="white",
                                font_weight="600",
                                border_radius="10px",
                                cursor="pointer",
                                _hover={"bg": "#B8864A"},
                                size="2",
                                on_click=AdminState.open_product_modal(0),
                            ),
                            spacing="2",
                        ),
                        width="100%",
                        align_items="center",
                        flex_wrap="wrap",
                        gap="8px",
                    ),
                    # Products table
                    rx.vstack(
                        rx.foreach(
                            AdminState.all_products,
                            lambda prod: rx.box(
                                rx.hstack(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.cond(
                                                prod["is_veg"],
                                                rx.text("🟢", font_size="10px"),
                                                rx.text("🔴", font_size="10px"),
                                            ),
                                            rx.text(
                                                prod["name"],
                                                font_weight="600",
                                                font_size="14px",
                                                color="#2B2B2B",
                                            ),
                                            rx.cond(
                                                prod["is_bestseller"],
                                                rx.box(
                                                    rx.text("⭐", font_size="10px"),
                                                    padding="2px 6px",
                                                    bg="#FEF3C7",
                                                    border_radius="8px",
                                                ),
                                            ),
                                            spacing="2",
                                            align_items="center",
                                        ),
                                        rx.text(
                                            f"₹{prod['price']}",
                                            font_size="13px",
                                            color="#D4A373",
                                            font_weight="600",
                                        ),
                                        rx.cond(
                                            prod["stock_quantity"] == 0,
                                            rx.box(
                                                rx.text("Sold Out", font_size="10px", font_weight="700", color="#EF4444"),
                                                bg="#FEE2E2",
                                                padding_x="6px",
                                                padding_y="1px",
                                                border_radius="6px",
                                            ),
                                            rx.cond(
                                                prod["is_low_stock"],
                                                rx.box(
                                                    rx.text(f"{prod['stock_quantity']} left", font_size="10px", font_weight="600", color="#D97706"),
                                                    bg="#FEF3C7",
                                                    padding_x="6px",
                                                    padding_y="1px",
                                                    border_radius="6px",
                                                ),
                                                rx.cond(
                                                    prod["is_unlimited"],
                                                    rx.text("∞", font_size="12px", color="#9CA3AF"),
                                                    rx.box(
                                                        rx.text(f"{prod['stock_quantity']} in stock", font_size="10px", font_weight="500", color="#059669"),
                                                        bg="#D1FAE5",
                                                        padding_x="6px",
                                                        padding_y="1px",
                                                        border_radius="6px",
                                                    ),
                                                ),
                                            ),
                                        ),
                                        spacing="1",
                                    ),
                                    rx.spacer(),
                                    rx.hstack(
                                        rx.button(
                                            rx.cond(
                                                prod["is_available"],
                                                rx.icon("eye", size=14),
                                                rx.icon("eye-off", size=14),
                                            ),
                                            size="1",
                                            variant="ghost",
                                            color=rx.cond(prod["is_available"], "#10B981", "#EF4444"),
                                            cursor="pointer",
                                            on_click=AdminState.toggle_product_availability(prod["id"]),
                                        ),
                                        rx.button(
                                            rx.icon("pencil", size=14),
                                            size="1",
                                            variant="ghost",
                                            color="#6B7280",
                                            cursor="pointer",
                                            on_click=AdminState.open_product_modal(prod["id"]),
                                        ),
                                        spacing="1",
                                    ),
                                    spacing="4",
                                    align_items="center",
                                    width="100%",
                                ),
                                bg="white",
                                border_radius="10px",
                                padding="14px 16px",
                                box_shadow="0 1px 3px rgba(0,0,0,0.04)",
                                width="100%",
                            ),
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    # Product Edit Modal
                    rx.dialog.root(
                        rx.dialog.content(
                            rx.dialog.title(
                                rx.cond(
                                    AdminState.edit_product_id > 0,
                                    "Edit Product",
                                    "Add New Product",
                                ),
                            ),
                            rx.vstack(
                                rx.input(
                                    placeholder="Product Name",
                                    value=AdminState.form_name,
                                    on_change=AdminState.set_form_name,
                                    width="100%",
                                ),
                                rx.text_area(
                                    placeholder="Description",
                                    value=AdminState.form_description,
                                    on_change=AdminState.set_form_description,
                                    width="100%",
                                ),
                                rx.input(
                                    placeholder="Price (₹)",
                                    value=AdminState.form_price,
                                    on_change=AdminState.set_form_price,
                                    type="number",
                                    width="100%",
                                ),
                                rx.input(
                                    placeholder="Image Filename (e.g., /chocolate.jpg)",
                                    value=AdminState.form_image_url,
                                    on_change=AdminState.set_form_image_url,
                                    width="100%",
                                ),
                                rx.input(
                                    placeholder="Weight Info (e.g., 500 g)",
                                    value=AdminState.form_weight_info,
                                    on_change=AdminState.set_form_weight_info,
                                    width="100%",
                                ),
                                rx.input(
                                    placeholder="Stock Quantity (-1 for unlimited)",
                                    value=AdminState.form_stock,
                                    on_change=AdminState.set_form_stock,
                                    type="number",
                                    width="100%",
                                ),
                                rx.cond(
                                    AdminState.error_message != "",
                                    rx.text(AdminState.error_message, color="#EF4444", font_size="13px"),
                                ),
                                rx.hstack(
                                    rx.dialog.close(
                                        rx.button(
                                            "Cancel",
                                            variant="outline",
                                            color="#6B7280",
                                            cursor="pointer",
                                            on_click=AdminState.close_product_modal,
                                        ),
                                    ),
                                    rx.button(
                                        "Save Product",
                                        bg="#D4A373",
                                        color="white",
                                        font_weight="600",
                                        cursor="pointer",
                                        _hover={"bg": "#B8864A"},
                                        on_click=AdminState.save_product,
                                    ),
                                    spacing="3",
                                    justify="end",
                                    width="100%",
                                ),
                                spacing="4",
                                width="100%",
                            ),
                            max_width="500px",
                        ),
                        open=AdminState.show_product_modal,
                    ),
                    spacing="6",
                    max_width="900px",
                    margin_x="auto",
                    padding_x="24px",
                    padding_y="32px",
                    width="100%",
                ),
            ),
            bg="#FEFAE0",
            width="100%",
            min_height="60vh",
        ),
        footer(),
        width="100%",
        min_height="100vh",
        bg="#FEFAE0",
        on_mount=AdminState.load_all_products,
    )


# =========================================================================
# Admin Users Page
# =========================================================================
def admin_users_page() -> rx.Component:
    """Admin user management page."""
    return rx.box(
        navbar(),
        rx.box(
            _admin_guard(
                rx.vstack(
                    rx.hstack(
                        rx.heading(
                            "Manage Users",
                            size="6",
                            color="#2B2B2B",
                            font_family="'Playfair Display', serif",
                        ),
                        rx.spacer(),
                        rx.link(
                            rx.button(
                                rx.icon("arrow-left", size=14),
                                "Dashboard",
                                variant="ghost",
                                color="#D4A373",
                                cursor="pointer",
                                size="2",
                            ),
                            href="/admin",
                        ),
                        width="100%",
                        align_items="center",
                    ),
                    rx.vstack(
                        rx.foreach(
                            AdminState.all_users,
                            lambda user: rx.box(
                                rx.hstack(
                                    rx.center(
                                        rx.icon("user", size=16, color="white"),
                                        width="36px",
                                        height="36px",
                                        bg="linear-gradient(135deg, #D4A373, #B8864A)",
                                        border_radius="50%",
                                        flex_shrink="0",
                                    ),
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text(
                                                user["full_name"],
                                                font_weight="600",
                                                font_size="14px",
                                                color="#2B2B2B",
                                            ),
                                            rx.cond(
                                                user["is_admin"],
                                                rx.box(
                                                    rx.text(
                                                        "Admin",
                                                        font_size="10px",
                                                        font_weight="600",
                                                        color="#7C3AED",
                                                    ),
                                                    bg="#EDE9FE",
                                                    padding_x="6px",
                                                    padding_y="1px",
                                                    border_radius="8px",
                                                ),
                                            ),
                                            rx.cond(
                                                user["is_verified"],
                                                rx.icon("circle-check", size=14, color="#10B981"),
                                                rx.icon("circle-x", size=14, color="#EF4444"),
                                            ),
                                            spacing="2",
                                            align_items="center",
                                        ),
                                        rx.text(
                                            user["email"],
                                            font_size="12px",
                                            color="#9CA3AF",
                                        ),
                                        spacing="0",
                                    ),
                                    rx.spacer(),
                                    rx.button(
                                        rx.cond(
                                            user["is_admin"],
                                            "Remove Admin",
                                            "Make Admin",
                                        ),
                                        size="1",
                                        variant="outline",
                                        border_radius="8px",
                                        cursor="pointer",
                                        color=rx.cond(user["is_admin"], "#EF4444", "#D4A373"),
                                        border_color=rx.cond(user["is_admin"], "#EF4444", "#D4A373"),
                                        on_click=AdminState.toggle_user_admin(user["id"]),
                                    ),
                                    spacing="3",
                                    align_items="center",
                                    width="100%",
                                ),
                                bg="white",
                                border_radius="10px",
                                padding="14px 16px",
                                box_shadow="0 1px 3px rgba(0,0,0,0.04)",
                                width="100%",
                            ),
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    spacing="6",
                    max_width="900px",
                    margin_x="auto",
                    padding_x="24px",
                    padding_y="32px",
                    width="100%",
                ),
            ),
            bg="#FEFAE0",
            width="100%",
            min_height="60vh",
        ),
        footer(),
        width="100%",
        min_height="100vh",
        bg="#FEFAE0",
        on_mount=AdminState.load_all_users,
    )
