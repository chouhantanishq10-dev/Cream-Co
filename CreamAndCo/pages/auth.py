"""
Cream & Co. — Authentication Pages
=====================================
Login, Register, Verify Email, Forgot Password, Reset Password pages.
"""

import reflex as rx
from ..components.navbar import navbar
from ..components.footer import footer
from ..states.auth_state import AuthState


def _auth_container(*children, **kwargs) -> rx.Component:
    """Shared layout wrapper for all auth pages."""
    return rx.box(
        navbar(),
        rx.center(
            rx.box(
                *children,
                width="100%",
                max_width="440px",
                bg="white",
                border_radius="20px",
                box_shadow="0 4px 24px rgba(0,0,0,0.08)",
                padding="40px",
            ),
            min_height="70vh",
            padding_x="24px",
            padding_y="48px",
        ),
        footer(),
        width="100%",
        bg="#FEFAE0",
        min_height="100vh",
    )


def _error_alert() -> rx.Component:
    """Conditional error message display."""
    return rx.cond(
        AuthState.error_message != "",
        rx.box(
            rx.hstack(
                rx.icon("circle-alert", size=16, color="#EF4444"),
                rx.text(
                    AuthState.error_message,
                    font_size="13px",
                    color="#EF4444",
                ),
                spacing="2",
            ),
            bg="#FEF2F2",
            border="1px solid #FECACA",
            border_radius="10px",
            padding="12px",
            width="100%",
        ),
    )


def _success_alert() -> rx.Component:
    """Conditional success message display."""
    return rx.cond(
        AuthState.success_message != "",
        rx.box(
            rx.hstack(
                rx.icon("circle-check", size=16, color="#10B981"),
                rx.text(
                    AuthState.success_message,
                    font_size="13px",
                    color="#10B981",
                ),
                spacing="2",
            ),
            bg="#F0FDF4",
            border="1px solid #BBF7D0",
            border_radius="10px",
            padding="12px",
            width="100%",
        ),
    )


# =========================================================================
# Login Page
# =========================================================================
def login_page() -> rx.Component:
    """Login page with email and password."""
    return _auth_container(
        rx.vstack(
            # Header
            rx.vstack(
                rx.text("🧁", font_size="36px"),
                rx.heading(
                    "Welcome Back",
                    size="5",
                    color="#2B2B2B",
                    font_family="'Playfair Display', serif",
                ),
                rx.text(
                    "Sign in to your Cream & Co. account",
                    color="#9CA3AF",
                    font_size="14px",
                ),
                spacing="2",
                align_items="center",
            ),
            _error_alert(),
            _success_alert(),
            # Form
            rx.vstack(
                rx.vstack(
                    rx.text("Email", font_size="13px", font_weight="500", color="#4B5563"),
                    rx.input(
                        placeholder="your@email.com",
                        value=AuthState.login_email,
                        on_change=AuthState.set_login_email,
                        type="email",
                        bg="white",
                        border="1px solid #E5E7EB",
                        border_radius="10px",
                        height="44px",
                        _focus={"border_color": "#D4A373", "box_shadow": "0 0 0 3px rgba(212,163,115,0.15)"},
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text("Password", font_size="13px", font_weight="500", color="#4B5563"),
                        rx.spacer(),
                        rx.link(
                            "Forgot password?",
                            href="/forgot-password",
                            font_size="12px",
                            color="#D4A373",
                            _hover={"color": "#B8864A"},
                        ),
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Enter your password",
                        value=AuthState.login_password,
                        on_change=AuthState.set_login_password,
                        type="password",
                        bg="white",
                        border="1px solid #E5E7EB",
                        border_radius="10px",
                        height="44px",
                        _focus={"border_color": "#D4A373", "box_shadow": "0 0 0 3px rgba(212,163,115,0.15)"},
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),
                rx.button(
                    rx.cond(
                        AuthState.is_loading,
                        rx.spinner(size="3"),
                        rx.text("Sign In"),
                    ),
                    width="100%",
                    height="44px",
                    bg="#D4A373",
                    color="white",
                    font_weight="600",
                    border_radius="10px",
                    cursor="pointer",
                    _hover={"bg": "#B8864A"},
                    on_click=AuthState.handle_login,
                    disabled=AuthState.is_loading,
                ),
                spacing="4",
                width="100%",
            ),
            # Register link
            rx.hstack(
                rx.text("Don't have an account?", font_size="13px", color="#9CA3AF"),
                rx.link(
                    "Sign up",
                    href="/register",
                    font_size="13px",
                    color="#D4A373",
                    font_weight="600",
                    _hover={"color": "#B8864A"},
                ),
                spacing="1",
                justify="center",
            ),
            spacing="6",
            width="100%",
        ),
    )


# =========================================================================
# OTP Verification Screen (shown after registration)
# =========================================================================
def _otp_verification_screen() -> rx.Component:
    """OTP code entry screen shown after signup."""
    return rx.vstack(
        rx.center(
            rx.icon("mail-check", size=32, color="#D4A373"),
            width="64px",
            height="64px",
            bg="#FAEDCD",
            border_radius="50%",
        ),
        rx.heading(
            "Verify Your Email",
            size="5",
            color="#2B2B2B",
            font_family="'Playfair Display', serif",
        ),
        rx.vstack(
            rx.text(
                "We sent a 6-digit code to",
                color="#9CA3AF",
                font_size="13px",
            ),
            rx.text(
                AuthState.pending_verification_email,
                color="#D4A373",
                font_weight="600",
                font_size="13px",
            ),
            spacing="1",
            align_items="center",
        ),
        _error_alert(),
        _success_alert(),
        rx.vstack(
            rx.text("Verification Code", font_size="13px", font_weight="500", color="#4B5563"),
            rx.input(
                placeholder="000000",
                value=AuthState.otp_code,
                on_change=AuthState.set_otp_code,
                max_length=6,
                bg="white",
                border="1px solid #E5E7EB",
                border_radius="10px",
                height="44px",
                font_size="18px",
                font_weight="600",
                text_align="center",
                letter_spacing="6px",
                _focus={
                    "border_color": "#D4A373",
                    "box_shadow": "0 0 0 3px rgba(212,163,115,0.15)",
                },
                _placeholder={"color": "#D1D5DB"},
                width="100%",
            ),
            spacing="1",
            width="100%",
        ),
        rx.vstack(
            rx.button(
                rx.cond(
                    AuthState.is_loading,
                    rx.spinner(size="3"),
                    rx.text("Verify & Continue"),
                ),
                width="100%",
                height="44px",
                bg="#D4A373",
                color="white",
                font_weight="600",
                border_radius="10px",
                cursor="pointer",
                _hover={"bg": "#B8864A"},
                on_click=AuthState.verify_otp,
                disabled=AuthState.is_loading,
            ),
            rx.hstack(
                rx.text("Didn't receive the code?", font_size="12px", color="#9CA3AF"),
                rx.text(
                    "Resend",
                    font_size="12px",
                    color="#D4A373",
                    font_weight="600",
                    cursor="pointer",
                    _hover={"color": "#B8864A", "text_decoration": "underline"},
                    on_click=AuthState.resend_otp,
                ),
                spacing="1",
                justify="center",
            ),
            spacing="3",
            width="100%",
        ),
        rx.text(
            "Code expires in 10 minutes",
            font_size="11px",
            color="#D1D5DB",
        ),
        spacing="5",
        align_items="center",
        width="100%",
    )


# =========================================================================
# Register Page
# =========================================================================
def register_page() -> rx.Component:
    """Registration page — shows form, then OTP screen after submit."""
    return _auth_container(
        rx.cond(
            AuthState.show_otp_screen,
            # OTP verification screen
            _otp_verification_screen(),
            # Registration form
            rx.vstack(
                rx.vstack(
                    rx.text("🧁", font_size="36px"),
                    rx.heading(
                        "Create Account",
                        size="5",
                        color="#2B2B2B",
                        font_family="'Playfair Display', serif",
                    ),
                    rx.text(
                        "Join Cream & Co. and start ordering",
                        color="#9CA3AF",
                        font_size="14px",
                    ),
                    spacing="2",
                    align_items="center",
                ),
                _error_alert(),
                _success_alert(),
                rx.vstack(
                    rx.vstack(
                        rx.text("Full Name", font_size="13px", font_weight="500", color="#4B5563"),
                        rx.input(
                            placeholder="Your full name",
                            value=AuthState.reg_name,
                            on_change=AuthState.set_reg_name,
                            bg="white",
                            border="1px solid #E5E7EB",
                            border_radius="10px",
                            height="44px",
                            _focus={"border_color": "#D4A373", "box_shadow": "0 0 0 3px rgba(212,163,115,0.15)"},
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Email", font_size="13px", font_weight="500", color="#4B5563"),
                        rx.input(
                            placeholder="your@email.com",
                            value=AuthState.reg_email,
                            on_change=AuthState.set_reg_email,
                            type="email",
                            bg="white",
                            border="1px solid #E5E7EB",
                            border_radius="10px",
                            height="44px",
                            _focus={"border_color": "#D4A373", "box_shadow": "0 0 0 3px rgba(212,163,115,0.15)"},
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Phone Number", font_size="13px", font_weight="500", color="#4B5563"),
                        rx.input(
                            placeholder="+91 9XXXXXXXXX",
                            value=AuthState.reg_phone,
                            on_change=AuthState.set_reg_phone,
                            type="tel",
                            bg="white",
                            border="1px solid #E5E7EB",
                            border_radius="10px",
                            height="44px",
                            _focus={"border_color": "#D4A373", "box_shadow": "0 0 0 3px rgba(212,163,115,0.15)"},
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Password", font_size="13px", font_weight="500", color="#4B5563"),
                        rx.input(
                            placeholder="Min 6 characters",
                            value=AuthState.reg_password,
                            on_change=AuthState.set_reg_password,
                            type="password",
                            bg="white",
                            border="1px solid #E5E7EB",
                            border_radius="10px",
                            height="44px",
                            _focus={"border_color": "#D4A373", "box_shadow": "0 0 0 3px rgba(212,163,115,0.15)"},
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Confirm Password", font_size="13px", font_weight="500", color="#4B5563"),
                        rx.input(
                            placeholder="Re-enter password",
                            value=AuthState.reg_confirm_password,
                            on_change=AuthState.set_reg_confirm_password,
                            type="password",
                            bg="white",
                            border="1px solid #E5E7EB",
                            border_radius="10px",
                            height="44px",
                            _focus={"border_color": "#D4A373", "box_shadow": "0 0 0 3px rgba(212,163,115,0.15)"},
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.button(
                        rx.cond(
                            AuthState.is_loading,
                            rx.spinner(size="3"),
                            rx.text("Create Account"),
                        ),
                        width="100%",
                        height="44px",
                        bg="#D4A373",
                        color="white",
                        font_weight="600",
                        border_radius="10px",
                        cursor="pointer",
                        _hover={"bg": "#B8864A"},
                        on_click=AuthState.handle_register,
                        disabled=AuthState.is_loading,
                    ),
                    spacing="3",
                    width="100%",
                ),
                rx.hstack(
                    rx.text("Already have an account?", font_size="13px", color="#9CA3AF"),
                    rx.link(
                        "Sign in",
                        href="/login",
                        font_size="13px",
                        color="#D4A373",
                        font_weight="600",
                        _hover={"color": "#B8864A"},
                    ),
                    spacing="1",
                    justify="center",
                ),
                spacing="5",
                width="100%",
            ),
        ),
    )


# =========================================================================
# Verify Email Page (OTP entry — also accessible directly)
# =========================================================================
def verify_email_page() -> rx.Component:
    """OTP verification page — users can enter code here too."""
    return _auth_container(
        _otp_verification_screen(),
    )


# =========================================================================
# Forgot Password Page
# =========================================================================
def forgot_password_page() -> rx.Component:
    """Forgot password — email input to send reset link."""
    return _auth_container(
        rx.vstack(
            rx.vstack(
                rx.text("🔑", font_size="36px"),
                rx.heading(
                    "Forgot Password?",
                    size="5",
                    color="#2B2B2B",
                    font_family="'Playfair Display', serif",
                ),
                rx.text(
                    "Enter your email and we'll send you a reset link",
                    color="#9CA3AF",
                    font_size="14px",
                    text_align="center",
                ),
                spacing="2",
                align_items="center",
            ),
            _error_alert(),
            _success_alert(),
            rx.vstack(
                rx.input(
                    placeholder="your@email.com",
                    value=AuthState.forgot_email,
                    on_change=AuthState.set_forgot_email,
                    type="email",
                    bg="white",
                    border="1px solid #E5E7EB",
                    border_radius="10px",
                    height="44px",
                    _focus={"border_color": "#D4A373", "box_shadow": "0 0 0 3px rgba(212,163,115,0.15)"},
                    width="100%",
                ),
                rx.button(
                    rx.cond(
                        AuthState.is_loading,
                        rx.spinner(size="3"),
                        rx.text("Send Reset Link"),
                    ),
                    width="100%",
                    height="44px",
                    bg="#D4A373",
                    color="white",
                    font_weight="600",
                    border_radius="10px",
                    cursor="pointer",
                    _hover={"bg": "#B8864A"},
                    on_click=AuthState.handle_forgot_password,
                    disabled=AuthState.is_loading,
                ),
                spacing="3",
                width="100%",
            ),
            rx.link(
                "Back to Login",
                href="/login",
                font_size="13px",
                color="#D4A373",
                font_weight="500",
            ),
            spacing="6",
            width="100%",
            align_items="center",
        ),
    )


# =========================================================================
# Reset Password Page
# =========================================================================
def reset_password_page() -> rx.Component:
    """Reset password page with new password form."""
    return _auth_container(
        rx.vstack(
            rx.vstack(
                rx.text("🔐", font_size="36px"),
                rx.heading(
                    "Reset Password",
                    size="5",
                    color="#2B2B2B",
                    font_family="'Playfair Display', serif",
                ),
                spacing="2",
                align_items="center",
            ),
            _error_alert(),
            _success_alert(),
            rx.vstack(
                rx.input(
                    placeholder="New password (min 6 chars)",
                    value=AuthState.reset_new_password,
                    on_change=AuthState.set_reset_new_password,
                    type="password",
                    bg="white",
                    border="1px solid #E5E7EB",
                    border_radius="10px",
                    height="44px",
                    _focus={"border_color": "#D4A373", "box_shadow": "0 0 0 3px rgba(212,163,115,0.15)"},
                    width="100%",
                ),
                rx.input(
                    placeholder="Confirm new password",
                    value=AuthState.reset_confirm_password,
                    on_change=AuthState.set_reset_confirm_password,
                    type="password",
                    bg="white",
                    border="1px solid #E5E7EB",
                    border_radius="10px",
                    height="44px",
                    _focus={"border_color": "#D4A373", "box_shadow": "0 0 0 3px rgba(212,163,115,0.15)"},
                    width="100%",
                ),
                rx.button(
                    rx.cond(
                        AuthState.is_loading,
                        rx.spinner(size="3"),
                        rx.text("Reset Password"),
                    ),
                    width="100%",
                    height="44px",
                    bg="#D4A373",
                    color="white",
                    font_weight="600",
                    border_radius="10px",
                    cursor="pointer",
                    _hover={"bg": "#B8864A"},
                    on_click=AuthState.handle_reset_password,
                    disabled=AuthState.is_loading,
                ),
                spacing="3",
                width="100%",
            ),
            spacing="6",
            width="100%",
        ),
    )
