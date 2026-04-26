"""
Cream & Co. — Cart & Checkout Pages
======================================
Shopping cart view and checkout flow.
"""

import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..states.cart_state import CartState
from ..states.order_state import OrderState
from ..states.auth_state import AuthState


def cart_page() -> rx.Component:
    """Shopping cart page with item management and checkout button."""
    return rx.box(
        navbar(),
        rx.box(
            rx.vstack(
                rx.heading(
                    "Your Cart",
                    size="6",
                    color="#2B2B2B",
                    font_family="'Playfair Display', serif",
                ),
                rx.cond(
                    CartState.is_cart_empty,
                    # Empty cart state
                    rx.center(
                        rx.vstack(
                            rx.text("🛒", font_size="64px", opacity="0.5"),
                            rx.heading(
                                "Your cart is empty",
                                size="4",
                                color="#6B7280",
                            ),
                            rx.text(
                                "Looks like you haven't added any treats yet!",
                                color="#9CA3AF",
                                font_size="14px",
                            ),
                            rx.link(
                                rx.button(
                                    "Browse Menu",
                                    bg="#D4A373",
                                    color="white",
                                    font_weight="600",
                                    border_radius="10px",
                                    cursor="pointer",
                                    _hover={"bg": "#B8864A"},
                                    size="3",
                                ),
                                href="/menu",
                            ),
                            spacing="4",
                            align_items="center",
                            padding_y="64px",
                        ),
                    ),
                    # Cart items
                    rx.flex(
                        # Items list
                        rx.vstack(
                            rx.foreach(
                                CartState.cart_items,
                                lambda item: rx.box(
                                    rx.hstack(
                                        # Product icon
                                        rx.center(
                                            rx.icon("cake-slice", size=24, color="#D4A373"),
                                            width="64px",
                                            height="64px",
                                            bg="#FAEDCD",
                                            border_radius="12px",
                                            flex_shrink="0",
                                        ),
                                        # Product details
                                        rx.vstack(
                                            rx.text(
                                                item["name"],
                                                font_weight="600",
                                                font_size="15px",
                                                color="#2B2B2B",
                                            ),
                                            rx.hstack(
                                                rx.cond(
                                                    item["is_veg"],
                                                    rx.text("🟢", font_size="10px"),
                                                    rx.text("🔴", font_size="10px"),
                                                ),
                                                rx.cond(
                                                    item["weight_info"] != "",
                                                    rx.text(
                                                        item["weight_info"],
                                                        font_size="11px",
                                                        color="#9CA3AF",
                                                    ),
                                                ),
                                                spacing="1",
                                            ),
                                            rx.text(
                                                f"₹{item['price']}",
                                                font_weight="600",
                                                color="#D4A373",
                                                font_size="14px",
                                            ),
                                            spacing="1",
                                            align_items="flex-start",
                                            flex="1",
                                        ),
                                        # Quantity controls
                                        rx.hstack(
                                            rx.button(
                                                rx.icon("minus", size=14),
                                                size="1",
                                                variant="outline",
                                                border_radius="8px",
                                                cursor="pointer",
                                                color="#6B7280",
                                                on_click=CartState.decrement_item(
                                                    item["cart_item_id"]
                                                ),
                                            ),
                                            rx.text(
                                                item["quantity"],
                                                font_weight="600",
                                                font_size="15px",
                                                color="#2B2B2B",
                                                min_width="28px",
                                                text_align="center",
                                            ),
                                            rx.button(
                                                rx.icon("plus", size=14),
                                                size="1",
                                                variant="outline",
                                                border_radius="8px",
                                                cursor="pointer",
                                                color="#6B7280",
                                                on_click=CartState.increment_item(
                                                    item["cart_item_id"]
                                                ),
                                            ),
                                            spacing="2",
                                            align_items="center",
                                        ),
                                        # Remove button
                                        rx.button(
                                            rx.icon("trash-2", size=16),
                                            size="1",
                                            variant="ghost",
                                            color="#EF4444",
                                            cursor="pointer",
                                            _hover={"bg": "#FEF2F2"},
                                            on_click=CartState.remove_from_cart(
                                                item["cart_item_id"]
                                            ),
                                        ),
                                        spacing="4",
                                        align_items="center",
                                        width="100%",
                                    ),
                                    padding="16px",
                                    bg="white",
                                    border_radius="12px",
                                    box_shadow="0 1px 4px rgba(0,0,0,0.04)",
                                    width="100%",
                                ),
                            ),
                            spacing="3",
                            width="100%",
                            flex="1",
                        ),
                        # Order summary sidebar
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "Order Summary",
                                    font_weight="600",
                                    font_size="16px",
                                    color="#2B2B2B",
                                ),
                                rx.divider(border_color="#E5E7EB"),
                                rx.hstack(
                                    rx.text("Subtotal", color="#6B7280", font_size="14px"),
                                    rx.spacer(),
                                    rx.text(
                                        f"₹{CartState.subtotal}",
                                        font_weight="500",
                                        color="#2B2B2B",
                                    ),
                                    width="100%",
                                ),
                                rx.hstack(
                                    rx.text("Delivery Fee", color="#6B7280", font_size="14px"),
                                    rx.spacer(),
                                    rx.cond(
                                        CartState.delivery_fee == 0,
                                        rx.text(
                                            "FREE",
                                            font_weight="600",
                                            color="#10B981",
                                            font_size="14px",
                                        ),
                                        rx.text(
                                            f"₹{CartState.delivery_fee}",
                                            font_weight="500",
                                            color="#2B2B2B",
                                        ),
                                    ),
                                    width="100%",
                                ),
                                rx.divider(border_color="#E5E7EB"),
                                rx.hstack(
                                    rx.text(
                                        "Total",
                                        font_weight="700",
                                        font_size="16px",
                                        color="#2B2B2B",
                                    ),
                                    rx.spacer(),
                                    rx.text(
                                        f"₹{CartState.total}",
                                        font_weight="700",
                                        font_size="20px",
                                        color="#D4A373",
                                    ),
                                    width="100%",
                                ),
                                rx.cond(
                                    CartState.subtotal < 500,
                                    rx.text(
                                        "Add more items for free delivery!",
                                        font_size="12px",
                                        color="#F59E0B",
                                        text_align="center",
                                    ),
                                ),
                                rx.link(
                                    rx.button(
                                        "Proceed to Checkout",
                                        rx.icon("arrow-right", size=16),
                                        width="100%",
                                        bg="#D4A373",
                                        color="white",
                                        font_weight="600",
                                        border_radius="10px",
                                        cursor="pointer",
                                        _hover={"bg": "#B8864A"},
                                        size="3",
                                    ),
                                    href="/checkout",
                                    width="100%",
                                ),
                                spacing="4",
                                width="100%",
                            ),
                            bg="white",
                            border_radius="16px",
                            padding="24px",
                            box_shadow="0 2px 12px rgba(0,0,0,0.06)",
                            width=["100%", "100%", "340px"],
                            flex_shrink="0",
                            position=["static", "static", "sticky"],
                            top="100px",
                        ),
                        direction="row",
                        wrap="wrap",
                        gap="24px",
                        width="100%",
                        align_items="flex-start",
                    ),
                ),
                spacing="6",
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
        on_mount=CartState.load_cart,
    )


# =========================================================================
# Checkout Page
# =========================================================================
def checkout_page() -> rx.Component:
    """Checkout page with delivery details and order placement."""
    return rx.box(
        navbar(),
        rx.box(
            rx.vstack(
                rx.heading(
                    "Checkout",
                    size="6",
                    color="#2B2B2B",
                    font_family="'Playfair Display', serif",
                ),
                rx.cond(
                    AuthState.is_authenticated,
                    rx.flex(
                        # Delivery form
                        rx.vstack(
                            rx.text(
                                "Delivery Details",
                                font_weight="600",
                                font_size="16px",
                                color="#2B2B2B",
                            ),
                            rx.vstack(
                                rx.text("Delivery Address *", font_size="13px", font_weight="500", color="#4B5563"),
                                rx.text_area(
                                    placeholder="Enter your full delivery address in Dewas",
                                    value=OrderState.checkout_address,
                                    on_change=OrderState.set_checkout_address,
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
                            rx.vstack(
                                rx.text("Phone Number *", font_size="13px", font_weight="500", color="#4B5563"),
                                rx.input(
                                    placeholder="+91 9XXXXXXXXX",
                                    value=OrderState.checkout_phone,
                                    on_change=OrderState.set_checkout_phone,
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
                                rx.text("Order Notes (Optional)", font_size="13px", font_weight="500", color="#4B5563"),
                                rx.text_area(
                                    placeholder="Any special instructions...",
                                    value=OrderState.checkout_notes,
                                    on_change=OrderState.set_checkout_notes,
                                    bg="white",
                                    border="1px solid #E5E7EB",
                                    border_radius="10px",
                                    min_height="60px",
                                    _focus={"border_color": "#D4A373"},
                                    width="100%",
                                ),
                                spacing="1",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.text("Payment Method", font_size="13px", font_weight="500", color="#4B5563"),
                                rx.hstack(
                                    rx.box(
                                        rx.hstack(
                                            rx.icon("banknote", size=18, color="#D4A373"),
                                            rx.text("Cash on Delivery", font_size="14px", font_weight="500"),
                                            spacing="2",
                                        ),
                                        padding="12px 16px",
                                        bg="white",
                                        border="2px solid #D4A373",
                                        border_radius="10px",
                                        cursor="pointer",
                                    ),
                                    spacing="3",
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            # Error/Success
                            rx.cond(
                                OrderState.error_message != "",
                                rx.box(
                                    rx.text(OrderState.error_message, color="#EF4444", font_size="13px"),
                                    bg="#FEF2F2",
                                    border_radius="10px",
                                    padding="12px",
                                    width="100%",
                                ),
                            ),
                            spacing="5",
                            flex="1",
                            width="100%",
                            bg="white",
                            border_radius="16px",
                            padding="24px",
                            box_shadow="0 2px 12px rgba(0,0,0,0.06)",
                        ),
                        # Order summary
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "Order Summary",
                                    font_weight="600",
                                    font_size="16px",
                                    color="#2B2B2B",
                                ),
                                rx.divider(border_color="#E5E7EB"),
                                rx.foreach(
                                    CartState.cart_items,
                                    lambda item: rx.hstack(
                                        rx.text(
                                            item["name"],
                                            font_size="13px",
                                            color="#6B7280",
                                            flex="1",
                                        ),
                                        rx.text(
                                            item["line_total"],
                                            font_size="13px",
                                            font_weight="500",
                                            color="#2B2B2B",
                                        ),
                                        width="100%",
                                    ),
                                ),
                                rx.divider(border_color="#E5E7EB"),
                                rx.hstack(
                                    rx.text("Subtotal", color="#6B7280", font_size="14px"),
                                    rx.spacer(),
                                    rx.text(f"₹{CartState.subtotal}", font_weight="500"),
                                    width="100%",
                                ),
                                rx.hstack(
                                    rx.text("Delivery", color="#6B7280", font_size="14px"),
                                    rx.spacer(),
                                    rx.cond(
                                        CartState.delivery_fee == 0,
                                        rx.text("FREE", color="#10B981", font_weight="600", font_size="14px"),
                                        rx.text(f"₹{CartState.delivery_fee}", font_weight="500"),
                                    ),
                                    width="100%",
                                ),
                                rx.divider(border_color="#E5E7EB"),
                                rx.hstack(
                                    rx.text("Total", font_weight="700", font_size="16px"),
                                    rx.spacer(),
                                    rx.text(
                                        f"₹{CartState.total}",
                                        font_weight="700",
                                        font_size="20px",
                                        color="#D4A373",
                                    ),
                                    width="100%",
                                ),
                                rx.button(
                                    rx.cond(
                                        OrderState.is_loading,
                                        rx.spinner(size="3"),
                                        rx.hstack(
                                            rx.icon("check", size=16),
                                            rx.text("Place Order"),
                                            spacing="2",
                                        ),
                                    ),
                                    width="100%",
                                    bg="#D4A373",
                                    color="white",
                                    font_weight="600",
                                    border_radius="10px",
                                    cursor="pointer",
                                    _hover={"bg": "#B8864A"},
                                    size="3",
                                    on_click=OrderState.place_order,
                                    disabled=OrderState.is_loading,
                                ),
                                spacing="4",
                            ),
                            bg="white",
                            border_radius="16px",
                            padding="24px",
                            box_shadow="0 2px 12px rgba(0,0,0,0.06)",
                            width=["100%", "100%", "360px"],
                            flex_shrink="0",
                        ),
                        direction="row",
                        wrap="wrap",
                        gap="24px",
                        width="100%",
                        align_items="flex-start",
                    ),
                    # Not authenticated
                    rx.center(
                        rx.vstack(
                            rx.text("Please log in to checkout.", color="#6B7280"),
                            rx.link(
                                rx.button(
                                    "Login",
                                    bg="#D4A373",
                                    color="white",
                                    border_radius="10px",
                                    cursor="pointer",
                                ),
                                href="/login",
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
            bg="#FEFAE0",
            width="100%",
            min_height="60vh",
        ),
        footer(),
        width="100%",
        min_height="100vh",
        bg="#FEFAE0",
        on_mount=[CartState.load_cart, OrderState.prefill_checkout],
    )
