"""
Cream & Co. — Navigation Bar Component
========================================
Responsive top navigation with cart icon, auth controls, and mobile menu.
"""

import reflex as rx
from ..states.auth_state import AuthState
from ..states.cart_state import CartState


def navbar() -> rx.Component:
    """Top navigation bar with logo, links, cart, and auth controls."""
    return rx.box(
        rx.box(
            rx.hstack(
                # ── Logo ──────────────────────────────────────────────
                rx.link(
                    rx.hstack(
                        rx.text("🧁", font_size="28px"),
                        rx.vstack(
                            rx.text(
                                "Cream & Co.",
                                font_weight="700",
                                font_size="20px",
                                color="#2B2B2B",
                                line_height="1.1",
                                font_family="'Playfair Display', serif",
                            ),
                            rx.text(
                                "Freshly Baked Happiness",
                                font_size="10px",
                                color="#9CA3AF",
                                line_height="1",
                            ),
                            spacing="0",
                            align_items="flex-start",
                        ),
                        spacing="3",
                        align_items="center",
                    ),
                    href="/",
                    _hover={"text_decoration": "none"},
                ),
                # ── Desktop Navigation Links ──────────────────────────
                rx.hstack(
                    rx.link(
                        "Home",
                        href="/",
                        color="#6B7280",
                        font_weight="500",
                        font_size="15px",
                        _hover={"color": "#D4A373"},
                        transition="color 0.2s",
                    ),
                    rx.link(
                        "Menu",
                        href="/menu",
                        color="#6B7280",
                        font_weight="500",
                        font_size="15px",
                        _hover={"color": "#D4A373"},
                        transition="color 0.2s",
                    ),
                    rx.link(
                        "About",
                        href="/about",
                        color="#6B7280",
                        font_weight="500",
                        font_size="15px",
                        _hover={"color": "#D4A373"},
                        transition="color 0.2s",
                    ),
                    rx.link(
                        "Contact",
                        href="/contact",
                        color="#6B7280",
                        font_weight="500",
                        font_size="15px",
                        _hover={"color": "#D4A373"},
                        transition="color 0.2s",
                    ),
                    spacing="6",
                    display=["none", "none", "flex", "flex"],
                ),
                # ── Right Section: Cart + Auth ────────────────────────
                rx.hstack(
                    # Cart icon
                    rx.link(
                        rx.box(
                            rx.icon("shopping-cart", size=22, color="#2B2B2B"),
                            rx.cond(
                                CartState.cart_count > 0,
                                rx.box(
                                    rx.text(
                                        CartState.cart_count,
                                        font_size="10px",
                                        font_weight="700",
                                        color="white",
                                    ),
                                    position="absolute",
                                    top="-6px",
                                    right="-6px",
                                    bg="#E63946",
                                    border_radius="50%",
                                    width="18px",
                                    height="18px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                ),
                            ),
                            position="relative",
                            cursor="pointer",
                            _hover={"transform": "scale(1.1)"},
                            transition="transform 0.2s",
                        ),
                        href="/cart",
                    ),
                    # Auth section
                    rx.cond(
                        AuthState.is_authenticated,
                        # Logged in — show user menu
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.button(
                                    rx.icon("user", size=16),
                                    rx.text(
                                        AuthState.user_name,
                                        display=["none", "none", "block"],
                                        font_size="14px",
                                    ),
                                    variant="ghost",
                                    color="#2B2B2B",
                                    cursor="pointer",
                                    _hover={"bg": "#FAEDCD"},
                                    border_radius="10px",
                                ),
                            ),
                            rx.menu.content(
                                rx.menu.item(
                                    rx.hstack(
                                        rx.icon("user", size=14),
                                        rx.text("My Profile"),
                                    ),
                                    on_click=rx.redirect("/account/profile"),
                                ),
                                rx.menu.item(
                                    rx.hstack(
                                        rx.icon("package", size=14),
                                        rx.text("My Orders"),
                                    ),
                                    on_click=rx.redirect("/account/orders"),
                                ),
                                rx.cond(
                                    AuthState.is_admin,
                                    rx.menu.item(
                                        rx.hstack(
                                            rx.icon("layout-dashboard", size=14),
                                            rx.text("Admin Panel"),
                                        ),
                                        on_click=rx.redirect("/admin"),
                                    ),
                                ),
                                rx.menu.separator(),
                                rx.menu.item(
                                    rx.hstack(
                                        rx.icon("log-out", size=14),
                                        rx.text("Logout"),
                                    ),
                                    on_click=AuthState.handle_logout,
                                    color="#EF4444",
                                ),
                                bg="white",
                                border_radius="12px",
                                box_shadow="0 4px 24px rgba(0,0,0,0.12)",
                            ),
                        ),
                        # Not logged in — show login/register
                        rx.hstack(
                            rx.link(
                                rx.button(
                                    "Login",
                                    variant="ghost",
                                    color="#D4A373",
                                    font_weight="600",
                                    cursor="pointer",
                                    _hover={"bg": "#FAEDCD"},
                                    border_radius="10px",
                                    size="2",
                                ),
                                href="/login",
                            ),
                            rx.link(
                                rx.button(
                                    "Sign Up",
                                    bg="#D4A373",
                                    color="white",
                                    font_weight="600",
                                    cursor="pointer",
                                    _hover={"bg": "#B8864A"},
                                    border_radius="10px",
                                    size="2",
                                ),
                                href="/register",
                            ),
                            spacing="2",
                            display=["none", "none", "flex", "flex"],
                        ),
                    ),
                    spacing="4",
                    align_items="center",
                ),
                justify="between",
                align_items="center",
                width="100%",
                max_width="1200px",
                margin_x="auto",
                padding_x="24px",
                padding_y="16px",
            ),
            width="100%",
        ),
        position="sticky",
        top="0",
        z_index="50",
        bg="rgba(255, 255, 255, 0.95)",
        backdrop_filter="blur(12px)",
        border_bottom="1px solid #F3F4F6",
        width="100%",
    )
