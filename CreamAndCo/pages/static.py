"""
Cream & Co. — About & Contact Pages
======================================
Static informational pages.
"""

import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..utils.constants import BUSINESS


# =========================================================================
# About Page
# =========================================================================
def about_page() -> rx.Component:
    """About Cream & Co. page."""
    return rx.box(
        navbar(),
        # Hero
        rx.box(
            rx.center(
                rx.vstack(
                    rx.text("🧁", font_size="48px"),
                    rx.heading(
                        "About Cream & Co.",
                        size="7",
                        color="white",
                        font_family="'Playfair Display', serif",
                    ),
                    rx.text(
                        "Our story, our passion, our promise",
                        color="#D1D5DB",
                        font_size="16px",
                    ),
                    spacing="3",
                    align_items="center",
                    padding_y="48px",
                ),
            ),
            bg="linear-gradient(135deg, #1F2937, #111827)",
            width="100%",
        ),
        # Content
        rx.box(
            rx.vstack(
                # Our Story
                rx.box(
                    rx.vstack(
                        rx.text(
                            "OUR STORY",
                            font_size="12px",
                            font_weight="600",
                            color="#D4A373",
                            letter_spacing="2px",
                        ),
                        rx.heading(
                            "Crafting Sweet Memories Since Day One",
                            size="5",
                            color="#2B2B2B",
                            font_family="'Playfair Display', serif",
                        ),
                        rx.text(
                            "Cream & Co. started with a simple dream — to bring freshly baked, "
                            "premium desserts to the heart of Dewas. What began as a small passion "
                            "project has grown into one of Dewas's most loved bakeries, serving "
                            "hundreds of happy customers every day.",
                            color="#6B7280",
                            font_size="15px",
                            line_height="1.8",
                        ),
                        rx.text(
                            "Located at 103, Mukti Marg, we take pride in using only the finest "
                            "ingredients — from Belgian chocolate to fresh cream and seasonal fruits. "
                            "Every item on our menu is handcrafted with care, ensuring that each "
                            "bite delivers the same warmth and joy we put into making it.",
                            color="#6B7280",
                            font_size="15px",
                            line_height="1.8",
                        ),
                        spacing="4",
                    ),
                    bg="white",
                    border_radius="16px",
                    padding="32px",
                    box_shadow="0 2px 12px rgba(0,0,0,0.06)",
                ),
                # Values
                rx.grid(
                    *[
                        rx.vstack(
                            rx.center(
                                rx.icon(item["icon"], size=28, color="white"),
                                width="56px",
                                height="56px",
                                bg="linear-gradient(135deg, #D4A373, #B8864A)",
                                border_radius="16px",
                            ),
                            rx.text(
                                item["title"],
                                font_weight="600",
                                font_size="16px",
                                color="#2B2B2B",
                            ),
                            rx.text(
                                item["desc"],
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
                        for item in [
                            {"icon": "award", "title": "Quality First", "desc": "Only the finest ingredients make it to your plate"},
                            {"icon": "heart", "title": "Made with Love", "desc": "Every item is handcrafted by our passionate bakers"},
                            {"icon": "shield-check", "title": "FSSAI Certified", "desc": f"License No. {BUSINESS['fssai']}"},
                            {"icon": "star", "title": "4.0 Rating", "desc": f"Trusted by {BUSINESS['total_ratings']}+ happy customers"},
                        ]
                    ],
                    columns=rx.breakpoints(initial="1", sm="2", md="4"),
                    spacing="4",
                    width="100%",
                ),
                spacing="8",
                max_width="1000px",
                margin_x="auto",
                padding_x="24px",
                padding_y="48px",
                width="100%",
            ),
            bg="#FEFAE0",
            width="100%",
        ),
        footer(),
        width="100%",
        min_height="100vh",
        bg="#FEFAE0",
    )


# =========================================================================
# Contact Page
# =========================================================================
def contact_page() -> rx.Component:
    """Contact page with business info and map."""
    return rx.box(
        navbar(),
        # Hero
        rx.box(
            rx.center(
                rx.vstack(
                    rx.heading(
                        "Get In Touch",
                        size="7",
                        color="white",
                        font_family="'Playfair Display', serif",
                    ),
                    rx.text(
                        "We'd love to hear from you",
                        color="#D1D5DB",
                        font_size="16px",
                    ),
                    spacing="3",
                    align_items="center",
                    padding_y="48px",
                ),
            ),
            bg="linear-gradient(135deg, #1F2937, #111827)",
            width="100%",
        ),
        # Content
        rx.box(
            rx.flex(
                # Contact Info Cards
                rx.vstack(
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.center(
                                    rx.icon("map-pin", size=20, color="white"),
                                    width="40px",
                                    height="40px",
                                    bg="#D4A373",
                                    border_radius="10px",
                                ),
                                rx.text("Visit Us", font_weight="600", font_size="16px", color="#2B2B2B"),
                                spacing="3",
                            ),
                            rx.text(
                                BUSINESS["address"],
                                color="#6B7280",
                                font_size="14px",
                                line_height="1.6",
                            ),
                            spacing="3",
                        ),
                        bg="white",
                        border_radius="16px",
                        padding="24px",
                        box_shadow="0 2px 12px rgba(0,0,0,0.06)",
                        width="100%",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.center(
                                    rx.icon("phone", size=20, color="white"),
                                    width="40px",
                                    height="40px",
                                    bg="#D4A373",
                                    border_radius="10px",
                                ),
                                rx.text("Call Us", font_weight="600", font_size="16px", color="#2B2B2B"),
                                spacing="3",
                            ),
                            rx.text(
                                BUSINESS["phone"],
                                color="#6B7280",
                                font_size="14px",
                            ),
                            rx.text(
                                "Available 10 AM - 10 PM, all days",
                                color="#9CA3AF",
                                font_size="12px",
                            ),
                            spacing="3",
                        ),
                        bg="white",
                        border_radius="16px",
                        padding="24px",
                        box_shadow="0 2px 12px rgba(0,0,0,0.06)",
                        width="100%",
                    ),
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.center(
                                    rx.icon("mail", size=20, color="white"),
                                    width="40px",
                                    height="40px",
                                    bg="#D4A373",
                                    border_radius="10px",
                                ),
                                rx.text("Email Us", font_weight="600", font_size="16px", color="#2B2B2B"),
                                spacing="3",
                            ),
                            rx.text(
                                BUSINESS["email"],
                                color="#6B7280",
                                font_size="14px",
                            ),
                            spacing="3",
                        ),
                        bg="white",
                        border_radius="16px",
                        padding="24px",
                        box_shadow="0 2px 12px rgba(0,0,0,0.06)",
                        width="100%",
                    ),
                    spacing="4",
                    width=["100%", "100%", "360px"],
                    flex_shrink="0",
                ),
                # Map embed
                rx.box(
                    rx.el.iframe(
                        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3666.1!2d76.05!3d22.96!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2sMukti+Marg+Dewas!5e0!3m2!1sen!2sin!4v1",
                        width="100%",
                        height="100%",
                        border="none",
                        border_radius="16px",
                    ),
                    width="100%",
                    height="400px",
                    border_radius="16px",
                    overflow="hidden",
                    box_shadow="0 2px 12px rgba(0,0,0,0.06)",
                    flex="1",
                ),
                direction="row",
                wrap="wrap",
                gap="24px",
                max_width="1000px",
                margin_x="auto",
                padding_x="24px",
                padding_y="48px",
                width="100%",
            ),
            bg="#FEFAE0",
            width="100%",
        ),
        footer(),
        width="100%",
        min_height="100vh",
        bg="#FEFAE0",
    )
