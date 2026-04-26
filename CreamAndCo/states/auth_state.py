"""
Cream & Co. — Authentication State
====================================
Handles registration with OTP email verification, login,
password reset, and session management using JWT tokens.
"""

import reflex as rx
import uuid
import random
from datetime import datetime, timedelta
from sqlmodel import select

from ..models.user import User
from ..services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)
from ..services.email_service import (
    send_otp_email,
    send_password_reset_email,
    notify_owner_new_signup,
)


class AuthState(rx.State):
    """Authentication state managing user sessions and auth flows."""

    # ── Session State ─────────────────────────────────────────────────────
    auth_token: str = ""
    user_id: str = ""
    user_email: str = ""
    user_name: str = ""
    user_phone: str = ""
    user_address: str = ""
    is_authenticated: bool = False
    is_admin: bool = False

    # ── UI State ──────────────────────────────────────────────────────────
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""

    # ── Form Fields ───────────────────────────────────────────────────────
    login_email: str = ""
    login_password: str = ""
    reg_name: str = ""
    reg_email: str = ""
    reg_phone: str = ""
    reg_password: str = ""
    reg_confirm_password: str = ""

    # ── OTP Verification ─────────────────────────────────────────────────
    otp_code: str = ""
    pending_verification_email: str = ""
    show_otp_screen: bool = False

    # ── Profile Edit ──────────────────────────────────────────────────────
    edit_name: str = ""
    edit_phone: str = ""
    edit_address: str = ""

    # ── Forgot Password ──────────────────────────────────────────────────
    forgot_email: str = ""
    reset_new_password: str = ""
    reset_confirm_password: str = ""

    def _clear_messages(self):
        self.error_message = ""
        self.success_message = ""

    # ── Explicit Setters (Reflex 0.9 compatibility) ───────────────────────
    @rx.event
    def set_login_email(self, value: str):
        self.login_email = value

    @rx.event
    def set_login_password(self, value: str):
        self.login_password = value

    @rx.event
    def set_reg_name(self, value: str):
        self.reg_name = value

    @rx.event
    def set_reg_email(self, value: str):
        self.reg_email = value

    @rx.event
    def set_reg_phone(self, value: str):
        self.reg_phone = value

    @rx.event
    def set_reg_password(self, value: str):
        self.reg_password = value

    @rx.event
    def set_reg_confirm_password(self, value: str):
        self.reg_confirm_password = value

    @rx.event
    def set_otp_code(self, value: str):
        self.otp_code = value

    @rx.event
    def set_edit_name(self, value: str):
        self.edit_name = value

    @rx.event
    def set_edit_phone(self, value: str):
        self.edit_phone = value

    @rx.event
    def set_edit_address(self, value: str):
        self.edit_address = value

    @rx.event
    def set_forgot_email(self, value: str):
        self.forgot_email = value

    @rx.event
    def set_reset_new_password(self, value: str):
        self.reset_new_password = value

    @rx.event
    def set_reset_confirm_password(self, value: str):
        self.reset_confirm_password = value

    # ─────────────────────────────────────────────────────────────────────
    # Registration (Step 1: Create account + send OTP)
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def handle_register(self):
        """Register a new user and send OTP for email verification."""
        self._clear_messages()
        self.is_loading = True

        if not self.reg_name.strip():
            self.error_message = "Full name is required."
            self.is_loading = False
            return
        if not self.reg_email.strip() or "@" not in self.reg_email:
            self.error_message = "Please enter a valid email address."
            self.is_loading = False
            return
        if len(self.reg_password) < 6:
            self.error_message = "Password must be at least 6 characters."
            self.is_loading = False
            return
        if self.reg_password != self.reg_confirm_password:
            self.error_message = "Passwords do not match."
            self.is_loading = False
            return

        try:
            with rx.session() as session:
                existing = session.exec(
                    select(User).where(
                        User.email == self.reg_email.strip().lower()
                    )
                ).first()
                if existing and existing.is_verified:
                    self.error_message = "An account with this email already exists."
                    self.is_loading = False
                    return

                # Generate 6-digit OTP
                otp = str(random.randint(100000, 999999))
                token_expires = (
                    datetime.utcnow() + timedelta(minutes=10)
                ).isoformat()

                if existing and not existing.is_verified:
                    # Update existing unverified account
                    existing.password_hash = hash_password(self.reg_password)
                    existing.full_name = self.reg_name.strip()
                    existing.phone = self.reg_phone.strip()
                    existing.verification_token = otp
                    existing.token_expires_at = token_expires
                    session.add(existing)
                else:
                    # Create new user (unverified)
                    user = User(
                        email=self.reg_email.strip().lower(),
                        password_hash=hash_password(self.reg_password),
                        full_name=self.reg_name.strip(),
                        phone=self.reg_phone.strip(),
                        verification_token=otp,
                        token_expires_at=token_expires,
                        is_verified=False,
                        is_admin=False,
                    )
                    session.add(user)

                session.commit()

                # Send OTP email via Brevo
                try:
                    send_otp_email(
                        to_email=self.reg_email.strip().lower(),
                        full_name=self.reg_name.strip(),
                        otp_code=otp,
                    )
                except Exception as e:
                    print(f"OTP email failed: {e}")

                # Send OTP via WhatsApp (if configured)
                if self.reg_phone.strip():
                    try:
                        from ..services.whatsapp_service import send_whatsapp_otp
                        send_whatsapp_otp(
                            phone=self.reg_phone.strip(),
                            otp_code=otp,
                        )
                    except Exception as e:
                        print(f"WhatsApp OTP failed: {e}")

                # Switch to OTP verification screen
                self.pending_verification_email = self.reg_email.strip().lower()
                self.show_otp_screen = True
                self.success_message = (
                    f"Verification code sent to {self.reg_email}!"
                )

        except Exception as e:
            self.error_message = "Registration failed. Please try again."
            print(f"Registration error: {e}")
        finally:
            self.is_loading = False

    # ─────────────────────────────────────────────────────────────────────
    # OTP Verification (Step 2)
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def verify_otp(self):
        """Verify the OTP code entered by user."""
        self._clear_messages()
        self.is_loading = True

        if len(self.otp_code.strip()) != 6:
            self.error_message = "Please enter the 6-digit code."
            self.is_loading = False
            return

        try:
            with rx.session() as session:
                user = session.exec(
                    select(User).where(
                        User.email == self.pending_verification_email,
                        User.verification_token == self.otp_code.strip(),
                    )
                ).first()

                if not user:
                    self.error_message = "Invalid verification code."
                    self.is_loading = False
                    return

                # Check expiry
                if user.token_expires_at:
                    expires = datetime.fromisoformat(user.token_expires_at)
                    if datetime.utcnow() > expires:
                        self.error_message = "Code expired. Please register again."
                        self.is_loading = False
                        return

                # Verify user
                user.is_verified = True
                user.verification_token = None
                user.token_expires_at = None
                user.updated_at = datetime.utcnow().isoformat()
                session.add(user)
                session.commit()

                # Notify owner of new signup
                try:
                    notify_owner_new_signup(
                        customer_name=user.full_name,
                        customer_email=user.email,
                    )
                except Exception:
                    pass

                self.success_message = "Email verified! You can now log in."
                self.show_otp_screen = False
                self.otp_code = ""
                self.pending_verification_email = ""

                # Clear registration form
                self.reg_name = ""
                self.reg_email = ""
                self.reg_phone = ""
                self.reg_password = ""
                self.reg_confirm_password = ""

        except Exception as e:
            self.error_message = "Verification failed. Please try again."
            print(f"OTP verification error: {e}")
        finally:
            self.is_loading = False

    @rx.event
    def resend_otp(self):
        """Resend OTP to the pending email."""
        self._clear_messages()
        if not self.pending_verification_email:
            return

        try:
            otp = str(random.randint(100000, 999999))
            token_expires = (
                datetime.utcnow() + timedelta(minutes=10)
            ).isoformat()

            with rx.session() as session:
                user = session.exec(
                    select(User).where(
                        User.email == self.pending_verification_email
                    )
                ).first()
                if user:
                    user.verification_token = otp
                    user.token_expires_at = token_expires
                    session.add(user)
                    session.commit()

                    send_otp_email(
                        to_email=user.email,
                        full_name=user.full_name,
                        otp_code=otp,
                    )
                    self.success_message = "New code sent!"
        except Exception as e:
            self.error_message = "Failed to resend code."
            print(f"Resend OTP error: {e}")

    # ─────────────────────────────────────────────────────────────────────
    # Login
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def handle_login(self):
        """Authenticate user with email and password."""
        self._clear_messages()
        self.is_loading = True

        if not self.login_email.strip() or not self.login_password:
            self.error_message = "Please enter your email and password."
            self.is_loading = False
            return

        try:
            with rx.session() as session:
                user = session.exec(
                    select(User).where(
                        User.email == self.login_email.strip().lower()
                    )
                ).first()

                if not user:
                    self.error_message = "Invalid email or password."
                    self.is_loading = False
                    return

                if not verify_password(self.login_password, user.password_hash):
                    self.error_message = "Invalid email or password."
                    self.is_loading = False
                    return

                if not user.is_verified:
                    self.error_message = "Please verify your email first."
                    self.is_loading = False
                    return

                # Generate JWT
                token = create_access_token(
                    user_id=user.id,
                    email=user.email,
                    is_admin=user.is_admin,
                    full_name=user.full_name,
                )

                self.auth_token = token
                self.user_id = user.id
                self.user_email = user.email
                self.user_name = user.full_name
                self.user_phone = user.phone
                self.user_address = user.address
                self.is_authenticated = True
                self.is_admin = user.is_admin

                self.login_email = ""
                self.login_password = ""
                self.success_message = f"Welcome back, {user.full_name}!"
                return rx.redirect("/")

        except Exception as e:
            self.error_message = "Login failed. Please try again."
            print(f"Login error: {e}")
        finally:
            self.is_loading = False

    # ─────────────────────────────────────────────────────────────────────
    # Session Restoration
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def check_auth(self):
        if not self.auth_token:
            return
        payload = decode_access_token(self.auth_token)
        if not payload:
            self.handle_logout()
            return
        self.user_id = payload.get("user_id", "")
        self.user_email = payload.get("email", "")
        self.user_name = payload.get("full_name", "")
        self.is_admin = payload.get("is_admin", False)
        self.is_authenticated = True

    # ─────────────────────────────────────────────────────────────────────
    # Logout
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def handle_logout(self):
        self.auth_token = ""
        self.user_id = ""
        self.user_email = ""
        self.user_name = ""
        self.user_phone = ""
        self.user_address = ""
        self.is_authenticated = False
        self.is_admin = False
        self._clear_messages()
        return rx.redirect("/")

    # ─────────────────────────────────────────────────────────────────────
    # Forgot Password
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def handle_forgot_password(self):
        self._clear_messages()
        self.is_loading = True

        if not self.forgot_email.strip():
            self.error_message = "Please enter your email address."
            self.is_loading = False
            return

        try:
            with rx.session() as session:
                user = session.exec(
                    select(User).where(
                        User.email == self.forgot_email.strip().lower()
                    )
                ).first()
                if user:
                    reset_token = str(uuid.uuid4())
                    user.reset_token = reset_token
                    user.reset_token_expires = (
                        datetime.utcnow() + timedelta(hours=1)
                    ).isoformat()
                    user.updated_at = datetime.utcnow().isoformat()
                    session.add(user)
                    session.commit()
                    send_password_reset_email(
                        to_email=user.email,
                        full_name=user.full_name,
                        token=reset_token,
                    )
                self.success_message = (
                    "If an account with that email exists, "
                    "we've sent a password reset link."
                )
                self.forgot_email = ""
        except Exception as e:
            self.error_message = "Something went wrong. Please try again."
            print(f"Forgot password error: {e}")
        finally:
            self.is_loading = False

    # ─────────────────────────────────────────────────────────────────────
    # Reset Password
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def handle_reset_password(self):
        self._clear_messages()
        self.is_loading = True

        params = self.router.page.params
        token = params.get("token", "")

        if not token:
            self.error_message = "Invalid reset link."
            self.is_loading = False
            return
        if len(self.reset_new_password) < 6:
            self.error_message = "Password must be at least 6 characters."
            self.is_loading = False
            return
        if self.reset_new_password != self.reset_confirm_password:
            self.error_message = "Passwords do not match."
            self.is_loading = False
            return

        try:
            with rx.session() as session:
                user = session.exec(
                    select(User).where(User.reset_token == token)
                ).first()
                if not user:
                    self.error_message = "Invalid or expired reset link."
                    self.is_loading = False
                    return
                if user.reset_token_expires:
                    expires = datetime.fromisoformat(user.reset_token_expires)
                    if datetime.utcnow() > expires:
                        self.error_message = "Reset link has expired."
                        self.is_loading = False
                        return
                user.password_hash = hash_password(self.reset_new_password)
                user.reset_token = None
                user.reset_token_expires = None
                user.updated_at = datetime.utcnow().isoformat()
                session.add(user)
                session.commit()
                self.success_message = "Password reset successful! You can now log in."
                self.reset_new_password = ""
                self.reset_confirm_password = ""
        except Exception as e:
            self.error_message = "Password reset failed. Please try again."
            print(f"Reset password error: {e}")
        finally:
            self.is_loading = False

    # ─────────────────────────────────────────────────────────────────────
    # Update Profile
    # ─────────────────────────────────────────────────────────────────────
    @rx.event
    def load_profile(self):
        self.edit_name = self.user_name
        self.edit_phone = self.user_phone
        self.edit_address = self.user_address

    @rx.event
    def handle_update_profile(self):
        self._clear_messages()
        self.is_loading = True
        if not self.user_id:
            self.error_message = "Not authenticated."
            self.is_loading = False
            return
        try:
            with rx.session() as session:
                user = session.exec(
                    select(User).where(User.id == self.user_id)
                ).first()
                if not user:
                    self.error_message = "User not found."
                    self.is_loading = False
                    return
                user.full_name = self.edit_name.strip()
                user.phone = self.edit_phone.strip()
                user.address = self.edit_address.strip()
                user.updated_at = datetime.utcnow().isoformat()
                session.add(user)
                session.commit()
                self.user_name = user.full_name
                self.user_phone = user.phone
                self.user_address = user.address
                self.success_message = "Profile updated successfully!"
        except Exception as e:
            self.error_message = "Failed to update profile."
            print(f"Profile update error: {e}")
        finally:
            self.is_loading = False

    # ─────────────────────────────────────────────────────────────────────
    # Change Password (OTP verified)
    # ─────────────────────────────────────────────────────────────────────
    change_pw_step: str = "idle"  # idle | otp_sent | done
    change_pw_otp: str = ""
    change_pw_new: str = ""
    change_pw_confirm: str = ""
    change_pw_message: str = ""
    change_pw_error: str = ""

    @rx.event
    def set_change_pw_otp(self, value: str):
        self.change_pw_otp = value

    @rx.event
    def set_change_pw_new(self, value: str):
        self.change_pw_new = value

    @rx.event
    def set_change_pw_confirm(self, value: str):
        self.change_pw_confirm = value

    @rx.event
    def send_change_password_otp(self):
        """Step 1: Send OTP to user's email for password change."""
        self.change_pw_error = ""
        self.change_pw_message = ""

        if not self.is_authenticated:
            self.change_pw_error = "Please log in first."
            return

        try:
            otp = str(random.randint(100000, 999999))
            with rx.session() as session:
                user = session.exec(
                    select(User).where(User.id == self.user_id)
                ).first()
                if not user:
                    self.change_pw_error = "User not found."
                    return
                user.verification_token = otp
                user.token_expires_at = (
                    datetime.utcnow() + timedelta(minutes=10)
                ).isoformat()
                session.add(user)
                session.commit()

                try:
                    send_otp_email(
                        to_email=user.email,
                        full_name=user.full_name,
                        otp_code=otp,
                    )
                except Exception as e:
                    print(f"Change password OTP email failed: {e}")

                # Send OTP via WhatsApp (if configured)
                if user.phone:
                    try:
                        from ..services.whatsapp_service import send_whatsapp_otp
                        send_whatsapp_otp(
                            phone=user.phone,
                            otp_code=otp,
                        )
                    except Exception as e:
                        print(f"WhatsApp OTP failed: {e}")

                self.change_pw_step = "otp_sent"
                self.change_pw_message = f"Code sent to {user.email}"
        except Exception as e:
            self.change_pw_error = "Failed to send code."
            print(f"Change password OTP error: {e}")

    @rx.event
    def verify_and_change_password(self):
        """Step 2: Verify OTP and update password."""
        self.change_pw_error = ""
        self.change_pw_message = ""

        if len(self.change_pw_otp.strip()) != 6:
            self.change_pw_error = "Enter the 6-digit code."
            return
        if len(self.change_pw_new) < 6:
            self.change_pw_error = "Password must be at least 6 characters."
            return
        if self.change_pw_new != self.change_pw_confirm:
            self.change_pw_error = "Passwords do not match."
            return

        try:
            with rx.session() as session:
                user = session.exec(
                    select(User).where(
                        User.id == self.user_id,
                        User.verification_token == self.change_pw_otp.strip(),
                    )
                ).first()

                if not user:
                    self.change_pw_error = "Invalid code."
                    return

                if user.token_expires_at:
                    expires = datetime.fromisoformat(user.token_expires_at)
                    if datetime.utcnow() > expires:
                        self.change_pw_error = "Code expired. Request a new one."
                        self.change_pw_step = "idle"
                        return

                user.password_hash = hash_password(self.change_pw_new)
                user.verification_token = None
                user.token_expires_at = None
                user.updated_at = datetime.utcnow().isoformat()
                session.add(user)
                session.commit()

                self.change_pw_step = "done"
                self.change_pw_message = "Password changed successfully!"
                self.change_pw_otp = ""
                self.change_pw_new = ""
                self.change_pw_confirm = ""

        except Exception as e:
            self.change_pw_error = "Failed to change password."
            print(f"Change password error: {e}")

    @rx.event
    def reset_change_password(self):
        """Reset change password flow."""
        self.change_pw_step = "idle"
        self.change_pw_otp = ""
        self.change_pw_new = ""
        self.change_pw_confirm = ""
        self.change_pw_message = ""
        self.change_pw_error = ""

