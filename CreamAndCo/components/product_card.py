"""
Cream & Co. — Product Card Component
======================================
Product card with image, details, price, and inline +/- cart controls.
Shows "Add" button when not in cart, shows - [qty] + when in cart.
"""

import reflex as rx
from ..states.cart_state import CartState


def _add_button(product: dict) -> rx.Component:
    """Add to cart button (shown when product is NOT in cart)."""
    return rx.button(
        rx.icon("plus", size=14),
        "Add",
        size="1",
        bg="#D4A373",
        color="white",
        border_radius="8px",
        font_weight="600",
        cursor="pointer",
        _hover={"bg": "#B8864A", "transform": "scale(1.05)"},
        transition="all 0.2s",
        on_click=CartState.add_to_cart(product["id"]),
    )


def _quantity_controls(product: dict) -> rx.Component:
    """Inline - [qty] + controls (shown when product IS in cart)."""
    return rx.hstack(
        rx.button(
            rx.icon("minus", size=12),
            size="1",
            variant="outline",
            border_color="#D4A373",
            color="#D4A373",
            border_radius="6px",
            cursor="pointer",
            _hover={"bg": "#FAEDCD"},
            on_click=CartState.decrement_product(product["id"]),
        ),
        rx.text(
            CartState.cart_quantities[product["id"].to(str)],
            font_weight="700",
            font_size="14px",
            color="#2B2B2B",
            min_width="24px",
            text_align="center",
        ),
        rx.button(
            rx.icon("plus", size=12),
            size="1",
            bg="#D4A373",
            color="white",
            border_radius="6px",
            cursor="pointer",
            _hover={"bg": "#B8864A"},
            on_click=CartState.add_to_cart(product["id"]),
        ),
        spacing="1",
        align_items="center",
        bg="#FFF8F0",
        padding="2px 4px",
        border_radius="8px",
        border="1px solid #FAEDCD",
    )


def product_card(product: dict) -> rx.Component:
    """Renders a single product card with inline cart controls."""
    return rx.box(
        rx.vstack(
            # Image section
            rx.box(
                rx.cond(
                    product["is_bestseller"],
                    rx.box(
                        rx.text(
                            "⭐ Bestseller",
                            font_size="10px",
                            font_weight="700",
                            color="white",
                        ),
                        position="absolute",
                        top="12px",
                        left="12px",
                        bg="#E63946",
                        padding_x="10px",
                        padding_y="4px",
                        border_radius="20px",
                        z_index="2",
                    ),
                ),
                # Veg badge
                rx.box(
                    rx.text(
                        rx.cond(product["is_veg"], "🟢", "🔴"),
                        font_size="14px",
                    ),
                    position="absolute",
                    top="12px",
                    right="12px",
                    bg="white",
                    padding="4px",
                    border_radius="50%",
                    box_shadow="0 2px 8px rgba(0,0,0,0.1)",
                    z_index="2",
                ),
                # Sold Out overlay
                rx.cond(
                    product["stock_quantity"] == 0,
                    rx.center(
                        rx.text(
                            "SOLD OUT",
                            font_size="16px",
                            font_weight="800",
                            color="white",
                            letter_spacing="2px",
                        ),
                        position="absolute",
                        top="0",
                        left="0",
                        width="100%",
                        height="100%",
                        bg="rgba(0,0,0,0.5)",
                        z_index="3",
                        border_radius="12px 12px 0 0",
                    ),
                ),
                # Product image or placeholder
                rx.cond(
                    product["image_url"] != "",
                    rx.image(
                        src=product["image_url"],
                        width="100%",
                        height="180px",
                        object_fit="cover",
                        border_radius="12px 12px 0 0",
                        loading="lazy",
                    ),
                    rx.center(
                        rx.icon(
                            "cake-slice",
                            size=48,
                            color="#D4A373",
                            opacity="0.5",
                        ),
                        width="100%",
                        height="180px",
                        bg="linear-gradient(135deg, #FAEDCD 0%, #FFF8F0 100%)",
                        border_radius="12px 12px 0 0",
                    ),
                ),
                position="relative",
                width="100%",
                overflow="hidden",
            ),
            # Details section
            rx.vstack(
                rx.text(
                    product["name"],
                    font_weight="600",
                    font_size="15px",
                    color="#2B2B2B",
                    line_height="1.3",
                    no_of_lines=2,
                ),
                rx.cond(
                    product["weight_info"] != "",
                    rx.text(
                        product["weight_info"],
                        font_size="12px",
                        color="#9CA3AF",
                        font_weight="500",
                    ),
                ),
                rx.text(
                    product["description"],
                    font_size="12px",
                    color="#9CA3AF",
                    no_of_lines=2,
                    line_height="1.4",
                ),
                # Low stock warning
                rx.cond(
                    product["is_low_stock"],
                    rx.text(
                        f"Only {product['stock_quantity']} left!",
                        font_size="11px",
                        font_weight="600",
                        color="#EF4444",
                    ),
                ),
                # Price + Cart controls
                rx.hstack(
                    rx.hstack(
                        rx.text(
                            rx.cond(
                                product["discount_price"],
                                f"₹{product['discount_price']}",
                                f"₹{product['price']}",
                            ),
                            font_weight="700",
                            font_size="18px",
                            color="#2B2B2B",
                        ),
                        rx.cond(
                            product["discount_price"],
                            rx.text(
                                f"₹{product['price']}",
                                font_size="13px",
                                color="#9CA3AF",
                                text_decoration="line-through",
                            ),
                        ),
                        spacing="2",
                        align_items="baseline",
                    ),
                    # Conditional: sold out / in cart / add
                    rx.cond(
                        product["stock_quantity"] == 0,
                        rx.text(
                            "Sold Out",
                            font_size="13px",
                            font_weight="700",
                            color="#EF4444",
                        ),
                        rx.cond(
                            CartState.cart_product_ids.contains(product["id"]),
                            _quantity_controls(product),
                            _add_button(product),
                        ),
                    ),
                    justify="between",
                    align_items="center",
                    width="100%",
                    margin_top="4px",
                ),
                spacing="2",
                padding="16px",
                align_items="flex-start",
                width="100%",
            ),
            spacing="0",
            width="100%",
        ),
        bg="white",
        border_radius="16px",
        overflow="hidden",
        box_shadow="0 2px 12px rgba(0,0,0,0.06)",
        _hover={
            "box_shadow": "0 8px 30px rgba(0,0,0,0.12)",
            "transform": "translateY(-4px)",
        },
        transition="all 0.3s ease",
        cursor="pointer",
        width="100%",
    )
