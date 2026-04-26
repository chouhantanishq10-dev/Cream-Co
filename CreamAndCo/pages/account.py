"""
Cream & Co. — Account Pages
==============================
User profile and order history pages (protected).
"""

import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..states.auth_state import AuthState
from ..states.order_state import OrderState
from ..utils.constants import ORDER_STATUSES


def _status_badge(status: str) -> rx.Component:
    """Render a colored badge for order status."""
    return rx.box(
        rx.text(
            status,
            font_size="11px",
            font_weight="600",
            text_transform="capitalize",
        ),
        padding_x="10px",
        padding_y="4px",
        border_radius="20px",
        bg=rx.match(
            status,
            ("pending", "#FEF3C7"),
            ("confirmed", "#DBEAFE"),
            ("preparing", "#EDE9FE"),
            ("out_for_delivery", "#CFFAFE"),
            ("delivered", "#D1FAE5"),
            ("cancelled", "#FEE2E2"),
            "#F3F4F6",
        ),
        color=rx.match(
            status,
            ("pending", "#D97706"),
            ("confirmed", "#2563EB"),
            ("preparing", "#7C3AED"),
            ("out_for_delivery", "#0891B2"),
            ("delivered", "#059669"),
            ("cancelled", "#DC2626"),
            "#6B7280",
        ),
    )


# =========================================================================
# Profile Page
# =========================================================================
def profile_page() -> rx.Component:
    """User profile view and edit page."""
    return rx.box(
        navbar(),
        rx.box(
            rx.cond(
                AuthState.is_authenticated,
                rx.vstack(
                    rx.heading(
                        "My Profile",
                        size="6",
                        color="#2B2B2B",
                        font_family="'Playfair Display', serif",
                    ),
                    rx.box(
                        rx.vstack(
                            # Profile header
                            rx.hstack(
                                rx.center(
                                    rx.icon("user", size=28, color="white"),
                                    width="64px",
                                    height="64px",
                                    bg="linear-gradient(135deg, #D4A373, #B8864A)",
                                    border_radius="50%",
                                ),
                                rx.vstack(
                                    rx.text(
                                        AuthState.user_name,
                                        font_weight="600",
                                        font_size="18px",
                                        color="#2B2B2B",
                                    ),
                                    rx.text(
                                        AuthState.user_email,
                                        font_size="14px",
                                        color="#9CA3AF",
                                    ),
                                    spacing="1",
                                ),
                                spacing="4",
                                align_items="center",
                            ),
                            rx.divider(border_color="#E5E7EB"),
                            # Edit form
                            rx.vstack(
                                rx.vstack(
                                    rx.text("Full Name", font_size="13px", font_weight="500", color="#4B5563"),
                                    rx.input(
                                        value=AuthState.edit_name,
                                        on_change=AuthState.set_edit_name,
                                        bg="white",
                                        border="1px solid #E5E7EB",
                                        border_radius="10px",
                                        height="44px",
                                        _focus={"border_color": "#D4A373"},
                                        width="100%",
                                    ),
                                    spacing="1",
                                    width="100%",
                                ),
                                rx.vstack(
                                    rx.text("Phone Number", font_size="13px", font_weight="500", color="#4B5563"),
                                    rx.input(
                                        value=AuthState.edit_phone,
                                        on_change=AuthState.set_edit_phone,
                                        type="tel",
                                        bg="white",
                                        border="1px solid #E5E7EB",
                                        border_radius="10px",
                                        height="44px",
                                        _focus={"border_color": "#D4A373"},
                                        width="100%",
                                    ),
                                    spacing="1",
                                    width="100%",
                                ),
                                rx.vstack(
                                    rx.text("Delivery Address", font_size="13px", font_weight="500", color="#4B5563"),
                                    rx.text_area(
                                        value=AuthState.edit_address,
                                        on_change=AuthState.set_edit_address,
                                        bg="white",
                                        border="1px solid #E5E7EB",
                                        border_radius="10px",
                                        min_height="80px",
                                        _focus={"border_color": "#D4A373"},
                                        width="100%",
                                    ),
                                    spacing="1",
                                    width="100%",
                                ),
                                spacing="4",
                                width="100%",
                            ),
                            # Messages
                            rx.cond(
                                AuthState.error_message != "",
                                rx.text(AuthState.error_message, color="#EF4444", font_size="13px"),
                            ),
                            rx.cond(
                                AuthState.success_message != "",
                                rx.text(AuthState.success_message, color="#10B981", font_size="13px"),
                            ),
                            rx.button(
                                rx.cond(
                                    AuthState.is_loading,
                                    rx.spinner(size="3"),
                                    rx.text("Save Changes"),
                                ),
                                bg="#D4A373",
                                color="white",
                                font_weight="600",
                                border_radius="10px",
                                cursor="pointer",
                                _hover={"bg": "#B8864A"},
                                width="100%",
                                on_click=AuthState.handle_update_profile,
                                disabled=AuthState.is_loading,
                            ),
                            spacing="5",
                            width="100%",
                        ),
                        bg="white",
                        border_radius="16px",
                        padding="32px",
                        box_shadow="0 2px 12px rgba(0,0,0,0.06)",
                        max_width="500px",
                        width="100%",
                    ),
                    # ── Change Password Card ──────────────────────────
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.icon("lock", size=20, color="#D4A373"),
                                rx.text(
                                    "Change Password",
                                    font_weight="600",
                                    font_size="16px",
                                    color="#2B2B2B",
                                ),
                                spacing="2",
                                align_items="center",
                            ),
                            rx.divider(border_color="#E5E7EB"),
                            # Error/Success messages
                            rx.cond(
                                AuthState.change_pw_error != "",
                                rx.box(
                                    rx.hstack(
                                        rx.icon("circle-alert", size=14, color="#EF4444"),
                                        rx.text(AuthState.change_pw_error, font_size="13px", color="#EF4444"),
                                        spacing="2",
                                    ),
                                    bg="#FEF2F2",
                                    border="1px solid #FECACA",
                                    border_radius="8px",
                                    padding="10px",
                                    width="100%",
                                ),
                            ),
                            rx.cond(
                                AuthState.change_pw_message != "",
                                rx.box(
                                    rx.hstack(
                                        rx.icon("circle-check", size=14, color="#10B981"),
                                        rx.text(AuthState.change_pw_message, font_size="13px", color="#10B981"),
                                        spacing="2",
                                    ),
                                    bg="#F0FDF4",
                                    border="1px solid #BBF7D0",
                                    border_radius="8px",
                                    padding="10px",
                                    width="100%",
                                ),
                            ),
                            # Step 1: Request OTP
                            rx.cond(
                                AuthState.change_pw_step == "idle",
                                rx.vstack(
                                    rx.text(
                                        "We'll send a verification code to your email before changing your password.",
                                        font_size="13px",
                                        color="#9CA3AF",
                                        line_height="1.5",
                                    ),
                                    rx.button(
                                        rx.icon("mail", size=14),
                                        "Send Verification Code",
                                        width="100%",
                                        bg="#D4A373",
                                        color="white",
                                        font_weight="600",
                                        border_radius="10px",
                                        cursor="pointer",
                                        _hover={"bg": "#B8864A"},
                                        on_click=AuthState.send_change_password_otp,
                                    ),
                                    spacing="3",
                                    width="100%",
                                ),
                            ),
                            # Step 2: Enter OTP + New Password
                            rx.cond(
                                AuthState.change_pw_step == "otp_sent",
                                rx.vstack(
                                    rx.vstack(
                                        rx.text("Verification Code", font_size="13px", font_weight="500", color="#4B5563"),
                                        rx.input(
                                            placeholder="000000",
                                            value=AuthState.change_pw_otp,
                                            on_change=AuthState.set_change_pw_otp,
                                            max_length=6,
                                            bg="white",
                                            border="1px solid #E5E7EB",
                                            border_radius="10px",
                                            height="44px",
                                            font_size="18px",
                                            font_weight="600",
                                            text_align="center",
                                            letter_spacing="6px",
                                            _focus={"border_color": "#D4A373"},
                                            _placeholder={"color": "#D1D5DB"},
                                            width="100%",
                                        ),
                                        spacing="1",
                                        width="100%",
                                    ),
                                    rx.vstack(
                                        rx.text("New Password", font_size="13px", font_weight="500", color="#4B5563"),
                                        rx.input(
                                            placeholder="Min 6 characters",
                                            value=AuthState.change_pw_new,
                                            on_change=AuthState.set_change_pw_new,
                                            type="password",
                                            bg="white",
                                            border="1px solid #E5E7EB",
                                            border_radius="10px",
                                            height="44px",
                                            _focus={"border_color": "#D4A373"},
                                            width="100%",
                                        ),
                                        spacing="1",
                                        width="100%",
                                    ),
                                    rx.vstack(
                                        rx.text("Confirm Password", font_size="13px", font_weight="500", color="#4B5563"),
                                        rx.input(
                                            placeholder="Re-enter password",
                                            value=AuthState.change_pw_confirm,
                                            on_change=AuthState.set_change_pw_confirm,
                                            type="password",
                                            bg="white",
                                            border="1px solid #E5E7EB",
                                            border_radius="10px",
                                            height="44px",
                                            _focus={"border_color": "#D4A373"},
                                            width="100%",
                                        ),
                                        spacing="1",
                                        width="100%",
                                    ),
                                    rx.button(
                                        "Change Password",
                                        width="100%",
                                        bg="#D4A373",
                                        color="white",
                                        font_weight="600",
                                        border_radius="10px",
                                        cursor="pointer",
                                        _hover={"bg": "#B8864A"},
                                        on_click=AuthState.verify_and_change_password,
                                    ),
                                    rx.text(
                                        "Cancel",
                                        font_size="12px",
                                        color="#9CA3AF",
                                        cursor="pointer",
                                        text_align="center",
                                        _hover={"color": "#6B7280"},
                                        on_click=AuthState.reset_change_password,
                                    ),
                                    spacing="3",
                                    width="100%",
                                ),
                            ),
                            # Step 3: Done
                            rx.cond(
                                AuthState.change_pw_step == "done",
                                rx.vstack(
                                    rx.center(
                                        rx.icon("circle-check", size=32, color="#10B981"),
                                        width="56px",
                                        height="56px",
                                        bg="#F0FDF4",
                                        border_radius="50%",
                                    ),
                                    rx.text(
                                        "Password changed successfully!",
                                        font_weight="600",
                                        color="#10B981",
                                        font_size="14px",
                                    ),
                                    rx.button(
                                        "Done",
                                        width="100%",
                                        variant="outline",
                                        color="#D4A373",
                                        border_color="#D4A373",
                                        border_radius="10px",
                                        cursor="pointer",
                                        on_click=AuthState.reset_change_password,
                                    ),
                                    spacing="3",
                                    align_items="center",
                                    width="100%",
                                ),
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        bg="white",
                        border_radius="16px",
                        padding="32px",
                        box_shadow="0 2px 12px rgba(0,0,0,0.06)",
                        max_width="500px",
                        width="100%",
                    ),
                    spacing="6",
                    max_width="1200px",
                    margin_x="auto",
                    padding_x="24px",
                    padding_y="32px",
                    width="100%",
                ),
                rx.center(
                    rx.vstack(
                        rx.text("Please log in to view your profile.", color="#6B7280"),
                        rx.link(rx.button("Login", bg="#D4A373", color="white", border_radius="10px", cursor="pointer"), href="/login"),
                        spacing="4",
                        align_items="center",
                        padding_y="64px",
                    ),
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
        on_mount=AuthState.load_profile,
    )


# =========================================================================
# Order History Page
# =========================================================================
def orders_page() -> rx.Component:
    """User's order history page."""
    return rx.box(
        navbar(),
        rx.box(
            rx.cond(
                AuthState.is_authenticated,
                rx.vstack(
                    rx.heading(
                        "My Orders",
                        size="6",
                        color="#2B2B2B",
                        font_family="'Playfair Display', serif",
                    ),
                    rx.cond(
                        OrderState.orders.length() > 0,
                        rx.vstack(
                            rx.foreach(
                                OrderState.orders,
                                lambda order: rx.box(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.vstack(
                                                rx.text(
                                                    order["order_number"],
                                                    font_weight="700",
                                                    font_size="16px",
                                                    color="#2B2B2B",
                                                ),
                                                rx.text(
                                                    order["created_at"],
                                                    font_size="12px",
                                                    color="#9CA3AF",
                                                ),
                                                spacing="1",
                                            ),
                                            rx.spacer(),
                                            _status_badge(order["status"]),
                                            width="100%",
                                            align_items="flex-start",
                                        ),
                                        rx.divider(border_color="#F3F4F6"),
                                        rx.text(
                                            order["items_summary"],
                                            font_size="13px",
                                            color="#6B7280",
                                            line_height="1.6",
                                        ),
                                        rx.divider(border_color="#F3F4F6"),
                                        rx.hstack(
                                            rx.text(
                                                "Total",
                                                font_weight="600",
                                                color="#2B2B2B",
                                            ),
                                            rx.spacer(),
                                            rx.text(
                                                order['total_amount'],
                                                font_weight="700",
                                                color="#D4A373",
                                                font_size="16px",
                                            ),
                                            width="100%",
                                        ),
                                        # Cancel button (only for pending/confirmed)
                                        rx.cond(
                                            (order["status"] == "pending") | (order["status"] == "confirmed"),
                                            rx.button(
                                                rx.icon("x", size=14),
                                                "Cancel Order",
                                                size="2",
                                                variant="outline",
                                                color="#EF4444",
                                                border_color="#FCA5A5",
                                                border_radius="8px",
                                                cursor="pointer",
                                                font_weight="500",
                                                _hover={"bg": "#FEF2F2"},
                                                width="100%",
                                                on_click=OrderState.cancel_order(order["id"]),
                                            ),
                                        ),
                                        spacing="3",
                                    ),
                                    bg="white",
                                    border_radius="16px",
                                    padding="20px",
                                    box_shadow="0 2px 12px rgba(0,0,0,0.04)",
                                    width="100%",
                                ),
                            ),
                            spacing="4",
                            width="100%",
                            max_width="700px",
                        ),
                        # No orders
                        rx.center(
                            rx.vstack(
                                rx.text("📦", font_size="48px", opacity="0.5"),
                                rx.text("No orders yet", font_weight="600", color="#6B7280"),
                                rx.link(
                                    rx.button(
                                        "Start Shopping",
                                        bg="#D4A373",
                                        color="white",
                                        border_radius="10px",
                                        cursor="pointer",
                                    ),
                                    href="/menu",
                                ),
                                spacing="4",
                                align_items="center",
                                padding_y="48px",
                            ),
                        ),
                    ),
                    spacing="6",
                    max_width="1200px",
                    margin_x="auto",
                    padding_x="24px",
                    padding_y="32px",
                    width="100%",
                ),
                rx.center(
                    rx.vstack(
                        rx.text("Please log in to view your orders.", color="#6B7280"),
                        rx.link(rx.button("Login", bg="#D4A373", color="white", border_radius="10px", cursor="pointer"), href="/login"),
                        spacing="4",
                        align_items="center",
                        padding_y="64px",
                    ),
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
        on_mount=OrderState.load_user_orders,
    )
