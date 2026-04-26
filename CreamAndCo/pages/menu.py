"""
Cream & Co. — Menu Page
=========================
Full product catalog with category filtering and search.
"""

import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..components.product_card import product_card
from ..states.product_state import ProductState


def menu_page() -> rx.Component:
    """Menu page with category tabs, search, and product grid."""
    return rx.box(
        navbar(),
        # Page header
        rx.box(
            rx.center(
                rx.vstack(
                    rx.text(
                        "OUR MENU",
                        font_size="12px",
                        font_weight="600",
                        color="#D4A373",
                        letter_spacing="2px",
                    ),
                    rx.heading(
                        "Discover Our Treats",
                        size="7",
                        color="white",
                        font_family="'Playfair Display', serif",
                    ),
                    rx.text(
                        "Explore our handcrafted selection of cakes, pastries, and desserts",
                        color="#D1D5DB",
                        font_size="15px",
                    ),
                    spacing="3",
                    align_items="center",
                    padding_y="48px",
                ),
            ),
            bg="linear-gradient(135deg, #1F2937, #111827)",
            width="100%",
        ),
        # Filters + Content
        rx.box(
            rx.vstack(
                # Search and Filters
                rx.flex(
                    # Search bar
                    rx.box(
                        rx.input(
                            placeholder="Search menu...",
                            value=ProductState.search_query,
                            on_change=ProductState.handle_search,
                            bg="white",
                            border="1px solid #E5E7EB",
                            border_radius="12px",
                            padding_x="16px",
                            height="44px",
                            font_size="14px",
                            _focus={
                                "border_color": "#D4A373",
                                "box_shadow": "0 0 0 3px rgba(212,163,115,0.15)",
                            },
                            width="100%",
                            max_width="400px",
                        ),
                        flex="1",
                    ),
                    # Category filter pills
                    rx.hstack(
                        rx.button(
                            "All",
                            size="2",
                            variant=rx.cond(
                                ProductState.selected_category == "all",
                                "solid",
                                "outline",
                            ),
                            bg=rx.cond(
                                ProductState.selected_category == "all",
                                "#D4A373",
                                "transparent",
                            ),
                            color=rx.cond(
                                ProductState.selected_category == "all",
                                "white",
                                "#6B7280",
                            ),
                            border_color="#E5E7EB",
                            border_radius="20px",
                            cursor="pointer",
                            font_weight="500",
                            _hover={"bg": rx.cond(
                                ProductState.selected_category == "all",
                                "#B8864A",
                                "#F9FAFB",
                            )},
                            on_click=ProductState.filter_by_category("all"),
                        ),
                        rx.foreach(
                            ProductState.categories,
                            lambda cat: rx.button(
                                cat["name"],
                                size="2",
                                variant=rx.cond(
                                    ProductState.selected_category == cat["slug"],
                                    "solid",
                                    "outline",
                                ),
                                bg=rx.cond(
                                    ProductState.selected_category == cat["slug"],
                                    "#D4A373",
                                    "transparent",
                                ),
                                color=rx.cond(
                                    ProductState.selected_category == cat["slug"],
                                    "white",
                                    "#6B7280",
                                ),
                                border_color="#E5E7EB",
                                border_radius="20px",
                                cursor="pointer",
                                font_weight="500",
                                _hover={"bg": rx.cond(
                                    ProductState.selected_category == cat["slug"],
                                    "#B8864A",
                                    "#F9FAFB",
                                )},
                                on_click=ProductState.filter_by_category(
                                    cat["slug"]
                                ),
                            ),
                        ),
                        spacing="2",
                        flex_wrap="wrap",
                    ),
                    direction="column",
                    gap="16px",
                    width="100%",
                    padding_y="24px",
                ),
                # Results count
                rx.text(
                    rx.cond(
                        ProductState.search_query != "",
                        f"Showing results for \"{ProductState.search_query}\"",
                        f"{ProductState.filtered_products.length()} items",
                    ),
                    font_size="13px",
                    color="#9CA3AF",
                ),
                # Product grid
                rx.cond(
                    ProductState.filtered_products.length() > 0,
                    rx.grid(
                        rx.foreach(
                            ProductState.filtered_products,
                            product_card,
                        ),
                        columns=rx.breakpoints(
                            initial="1", sm="2", md="3", lg="4"
                        ),
                        spacing="5",
                        width="100%",
                    ),
                    # Empty state
                    rx.center(
                        rx.vstack(
                            rx.icon(
                                "search",
                                size=48,
                                color="#D4A373",
                                opacity="0.5",
                            ),
                            rx.text(
                                "No products found",
                                font_weight="600",
                                font_size="18px",
                                color="#2B2B2B",
                            ),
                            rx.text(
                                "Try adjusting your search or filters",
                                font_size="14px",
                                color="#9CA3AF",
                            ),
                            spacing="3",
                            align_items="center",
                            padding_y="48px",
                        ),
                    ),
                ),
                spacing="4",
                max_width="1200px",
                margin_x="auto",
                padding_x="24px",
                padding_y="32px",
                width="100%",
            ),
            bg="#FEFAE0",
            width="100%",
            min_height="60vh",
        ),
        footer(),
        width="100%",
        min_height="100vh",
        bg="#FEFAE0",
        on_mount=ProductState.load_products,
    )
