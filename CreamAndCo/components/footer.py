"""
Cream & Co. — Footer Component
================================
Site-wide footer with business info, links, and FSSAI license.
"""

import reflex as rx
from ..utils.constants import BUSINESS


def footer() -> rx.Component:
    """Site footer with branding, links, contact info, and legal."""
    return rx.box(
        rx.box(
            rx.vstack(
                # Top section
                rx.flex(
                    # Brand column
                    rx.vstack(
                        rx.hstack(
                            rx.text("🧁", font_size="24px"),
                            rx.text(
                                "Cream & Co.",
                                font_weight="700",
                                font_size="22px",
                                color="white",
                                font_family="'Playfair Display', serif",
                            ),
                            spacing="2",
                        ),
                        rx.text(
                            BUSINESS["tagline"],
                            color="#D4A373",
                            font_size="14px",
                            font_weight="500",
                        ),
                        rx.text(
                            "Your favorite neighborhood bakery in Dewas, "
                            "crafting fresh, delicious baked goods with love "
                            "since day one.",
                            color="#9CA3AF",
                            font_size="13px",
                            line_height="1.6",
                            max_width="300px",
                        ),
                        spacing="3",
                        align_items="flex-start",
                    ),
                    # Quick Links
                    rx.vstack(
                        rx.text(
                            "Quick Links",
                            font_weight="600",
                            color="white",
                            font_size="15px",
                            margin_bottom="8px",
                        ),
                        rx.link("Home", href="/", color="#9CA3AF", font_size="13px", _hover={"color": "#D4A373"}),
                        rx.link("Menu", href="/menu", color="#9CA3AF", font_size="13px", _hover={"color": "#D4A373"}),
                        rx.link("About Us", href="/about", color="#9CA3AF", font_size="13px", _hover={"color": "#D4A373"}),
                        rx.link("Contact", href="/contact", color="#9CA3AF", font_size="13px", _hover={"color": "#D4A373"}),
                        spacing="2",
                        align_items="flex-start",
                    ),
                    # Contact Info
                    rx.vstack(
                        rx.text(
                            "Contact Us",
                            font_weight="600",
                            color="white",
                            font_size="15px",
                            margin_bottom="8px",
                        ),
                        rx.hstack(
                            rx.icon("map-pin", size=14, color="#D4A373"),
                            rx.text(
                                BUSINESS["address"],
                                color="#9CA3AF",
                                font_size="13px",
                                max_width="220px",
                            ),
                            spacing="2",
                            align_items="flex-start",
                        ),
                        rx.hstack(
                            rx.icon("phone", size=14, color="#D4A373"),
                            rx.text(
                                BUSINESS["phone"],
                                color="#9CA3AF",
                                font_size="13px",
                            ),
                            spacing="2",
                        ),
                        rx.hstack(
                            rx.icon("mail", size=14, color="#D4A373"),
                            rx.text(
                                BUSINESS["email"],
                                color="#9CA3AF",
                                font_size="13px",
                            ),
                            spacing="2",
                        ),
                        spacing="3",
                        align_items="flex-start",
                    ),
                    direction="row",
                    wrap="wrap",
                    gap="48px",
                    width="100%",
                ),
                # Divider
                rx.divider(border_color="#374151", margin_y="24px"),
                # Bottom section
                rx.flex(
                    rx.text(
                        "© 2024 Cream & Co. All rights reserved.",
                        color="#6B7280",
                        font_size="12px",
                    ),
                    rx.hstack(
                        rx.text("FSSAI Lic. No.", color="#6B7280", font_size="12px"),
                        rx.text(
                            BUSINESS["fssai"],
                            color="#D4A373",
                            font_size="12px",
                            font_weight="600",
                        ),
                        spacing="1",
                    ),
                    justify="between",
                    align_items="center",
                    width="100%",
                    flex_wrap="wrap",
                    gap="12px",
                ),
                spacing="0",
                width="100%",
            ),
            max_width="1200px",
            margin_x="auto",
            padding_x="24px",
            padding_y="48px",
            width="100%",
        ),
        bg="#1F2937",
        width="100%",
        margin_top="auto",
    )
