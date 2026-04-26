"""
Cream & Co. — Home Page
=========================
Landing page with hero, category showcase, bestsellers, and features.
"""

import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..components.product_card import product_card
from ..states.product_state import ProductState
from ..utils.constants import BUSINESS, COLORS


def hero_section() -> rx.Component:
    """Full-width hero banner with CTA buttons."""
    return rx.box(
        rx.center(
            rx.vstack(
                rx.box(
                    rx.text(
                        "FSSAI Certified",
                        font_size="11px",
                        font_weight="600",
                        color="#D4A373",
                        letter_spacing="1.5px",
                        text_transform="uppercase",
                    ),
                    bg="rgba(212, 163, 115, 0.15)",
                    padding_x="16px",
                    padding_y="6px",
                    border_radius="20px",
                    border="1px solid rgba(212, 163, 115, 0.3)",
                ),
                rx.heading(
                    "Freshly Baked",
                    size="9",
                    color="white",
                    font_family="'Playfair Display', serif",
                    font_weight="700",
                    text_align="center",
                    line_height="1.1",
                ),
                rx.heading(
                    "Happiness, Delivered!",
                    size="7",
                    color="#D4A373",
                    font_family="'Playfair Display', serif",
                    font_weight="600",
                    text_align="center",
                ),
                rx.text(
                    "Artisan cakes, pastries, and desserts crafted with love "
                    "in Dewas. From our oven to your doorstep.",
                    color="#D1D5DB",
                    font_size="16px",
                    text_align="center",
                    max_width="500px",
                    line_height="1.7",
                ),
                rx.hstack(
                    rx.link(
                        rx.button(
                            rx.icon("shopping-bag", size=18),
                            "Order Now",
                            size="3",
                            bg="#D4A373",
                            color="white",
                            font_weight="600",
                            border_radius="12px",
                            cursor="pointer",
                            _hover={"bg": "#B8864A", "transform": "translateY(-2px)"},
                            transition="all 0.3s",
                            box_shadow="0 4px 14px rgba(212, 163, 115, 0.4)",
                        ),
                        href="/menu",
                    ),
                    rx.link(
                        rx.button(
                            "View Menu",
                            rx.icon("arrow-right", size=16),
                            size="3",
                            variant="outline",
                            color="white",
                            border_color="white",
                            font_weight="600",
                            border_radius="12px",
                            cursor="pointer",
                            _hover={"bg": "rgba(255,255,255,0.1)"},
                        ),
                        href="/menu",
                    ),
                    spacing="4",
                    margin_top="8px",
                ),
                # Rating badge
                rx.hstack(
                    rx.hstack(
                        rx.icon("star", size=16, color="#FBBF24", fill="#FBBF24"),
                        rx.text(
                            str(BUSINESS["rating"]),
                            font_weight="700",
                            color="white",
                            font_size="15px",
                        ),
                        spacing="1",
                    ),
                    rx.text("•", color="#6B7280"),
                    rx.text(
                        f"{BUSINESS['total_ratings']}+ happy customers",
                        color="#9CA3AF",
                        font_size="13px",
                    ),
                    spacing="2",
                    margin_top="16px",
                    bg="rgba(255,255,255,0.08)",
                    padding_x="16px",
                    padding_y="8px",
                    border_radius="20px",
                ),
                spacing="4",
                align_items="center",
                padding_y="80px",
                padding_x="24px",
            ),
        ),
        bg="linear-gradient(135deg, #1F2937 0%, #111827 50%, #0F172A 100%)",
        width="100%",
        min_height="550px",
        position="relative",
        overflow="hidden",
    )


def category_section() -> rx.Component:
    """Category showcase with cards."""
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.text(
                    "OUR CATEGORIES",
                    font_size="12px",
                    font_weight="600",
                    color="#D4A373",
                    letter_spacing="2px",
                ),
                rx.heading(
                    "Explore Our Menu",
                    size="6",
                    color="#2B2B2B",
                    font_family="'Playfair Display', serif",
                ),
                spacing="2",
                align_items="center",
            ),
            rx.grid(
                rx.foreach(
                    ProductState.categories,
                    lambda cat: rx.link(
                        rx.box(
                            rx.center(
                                rx.icon(
                                    "cake-slice",
                                    size=36,
                                    color="#D4A373",
                                ),
                                width="72px",
                                height="72px",
                                bg="#FAEDCD",
                                border_radius="20px",
                                margin_bottom="12px",
                            ),
                            rx.text(
                                cat["name"],
                                font_weight="600",
                                font_size="16px",
                                color="#2B2B2B",
                                text_align="center",
                            ),
                            rx.text(
                                cat["description"],
                                font_size="12px",
                                color="#9CA3AF",
                                text_align="center",
                                no_of_lines=2,
                            ),
                            padding="24px",
                            bg="white",
                            border_radius="16px",
                            box_shadow="0 2px 12px rgba(0,0,0,0.04)",
                            _hover={
                                "box_shadow": "0 8px 30px rgba(0,0,0,0.1)",
                                "transform": "translateY(-4px)",
                            },
                            transition="all 0.3s ease",
                            text_align="center",
                        ),
                        href="/menu",
                        _hover={"text_decoration": "none"},
                    ),
                ),
                columns=rx.breakpoints(initial="2", md="4"),
                spacing="5",
                width="100%",
            ),
            spacing="8",
            align_items="center",
            max_width="1200px",
            margin_x="auto",
            padding_x="24px",
            padding_y="64px",
        ),
        bg="#FEFAE0",
        width="100%",
    )


def bestsellers_section() -> rx.Component:
    """Bestseller products grid."""
    return rx.box(
        rx.vstack(
            rx.vstack(
                rx.text(
                    "CUSTOMER FAVORITES",
                    font_size="12px",
                    font_weight="600",
                    color="#D4A373",
                    letter_spacing="2px",
                ),
                rx.heading(
                    "Our Bestsellers",
                    size="6",
                    color="#2B2B2B",
                    font_family="'Playfair Display', serif",
                ),
                spacing="2",
                align_items="center",
            ),
            rx.grid(
                rx.foreach(
                    ProductState.bestsellers,
                    product_card,
                ),
                columns=rx.breakpoints(initial="1", sm="2", md="3", lg="4"),
                spacing="5",
                width="100%",
            ),
            rx.link(
                rx.button(
                    "View Full Menu",
                    rx.icon("arrow-right", size=16),
                    size="3",
                    variant="outline",
                    color="#D4A373",
                    border_color="#D4A373",
                    font_weight="600",
                    border_radius="12px",
                    cursor="pointer",
                    _hover={"bg": "#FAEDCD"},
                ),
                href="/menu",
            ),
            spacing="8",
            align_items="center",
            max_width="1200px",
            margin_x="auto",
            padding_x="24px",
            padding_y="64px",
        ),
        width="100%",
    )


def features_section() -> rx.Component:
    """'Why Choose Us' features grid."""
    features = [
        {"icon": "leaf", "title": "Fresh Ingredients", "desc": "Every item made with premium, fresh ingredients sourced daily"},
        {"icon": "truck", "title": "Fast Delivery", "desc": "Quick delivery across Dewas to your doorstep"},
        {"icon": "shield-check", "title": "FSSAI Certified", "desc": "Licensed and certified for your safety and trust"},
        {"icon": "heart", "title": "Made with Love", "desc": "Handcrafted by passionate bakers who care about every bite"},
    ]
    return rx.box(
        rx.vstack(
            rx.heading(
                "Why Choose Cream & Co.?",
                size="6",
                color="#2B2B2B",
                font_family="'Playfair Display', serif",
                text_align="center",
            ),
            rx.grid(
                *[
                    rx.vstack(
                        rx.center(
                            rx.icon(f["icon"], size=28, color="white"),
                            width="56px",
                            height="56px",
                            bg="linear-gradient(135deg, #D4A373, #B8864A)",
                            border_radius="16px",
                        ),
                        rx.text(
                            f["title"],
                            font_weight="600",
                            font_size="16px",
                            color="#2B2B2B",
                        ),
                        rx.text(
                            f["desc"],
                            font_size="13px",
                            color="#9CA3AF",
                            text_align="center",
                            line_height="1.5",
                        ),
                        align_items="center",
                        padding="24px",
                        bg="white",
                        border_radius="16px",
                        box_shadow="0 2px 12px rgba(0,0,0,0.04)",
                        spacing="3",
                    )
                    for f in features
                ],
                columns=rx.breakpoints(initial="1", sm="2", md="4"),
                spacing="5",
                width="100%",
            ),
            spacing="8",
            align_items="center",
            max_width="1200px",
            margin_x="auto",
            padding_x="24px",
            padding_y="64px",
        ),
        bg="#F9FAFB",
        width="100%",
    )


def cta_section() -> rx.Component:
    """Call-to-action banner."""
    return rx.box(
        rx.center(
            rx.vstack(
                rx.heading(
                    "Ready to Order?",
                    size="6",
                    color="white",
                    font_family="'Playfair Display', serif",
                ),
                rx.text(
                    "Browse our menu and get your favorite treats delivered in Dewas!",
                    color="#D1D5DB",
                    text_align="center",
                    font_size="15px",
                ),
                rx.link(
                    rx.button(
                        rx.icon("shopping-bag", size=18),
                        "Order Now",
                        size="3",
                        bg="#D4A373",
                        color="white",
                        font_weight="600",
                        border_radius="12px",
                        cursor="pointer",
                        _hover={"bg": "#B8864A"},
                        box_shadow="0 4px 14px rgba(212, 163, 115, 0.4)",
                    ),
                    href="/menu",
                ),
                spacing="4",
                align_items="center",
                padding_y="48px",
                padding_x="24px",
            ),
        ),
        bg="linear-gradient(135deg, #1F2937, #111827)",
        width="100%",
    )


def index() -> rx.Component:
    """Home page layout."""
    return rx.box(
        navbar(),
        hero_section(),
        category_section(),
        bestsellers_section(),
        features_section(),
        cta_section(),
        footer(),
        width="100%",
        min_height="100vh",
        bg="#FEFAE0",
        on_mount=ProductState.load_products,
    )
