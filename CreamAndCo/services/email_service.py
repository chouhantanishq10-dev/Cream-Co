"""
Cream & Co. — Email Service (Brevo)
======================================
Production email delivery via Brevo (formerly Sendinblue) API.
Free tier: 300 emails/day — no domain verification needed.
Just verify your sender email at https://app.brevo.com

Setup:
  1. Sign up at https://brevo.com (free)
  2. Verify your sender email (Settings → Senders → Add Sender → click verification link)
  3. Get API key from Settings → SMTP & API → API Keys
  4. Add to .env: BREVO_API_KEY=your-key
"""

import os
import requests

# ---------------------------------------------------------------------------
# Brevo Configuration
# ---------------------------------------------------------------------------
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply@creamandco.in")
SENDER_NAME = os.getenv("SENDER_NAME", "Cream & Co.")
OWNER_EMAIL = os.getenv("OWNER_NOTIFICATION_EMAIL", "")
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:3000")

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def _send_email(
    to_email: str,
    subject: str,
    html_body: str,
    attachment: dict | None = None,
) -> bool:
    """Send an email via Brevo API. Optional attachment dict: {content, name}."""
    if not BREVO_API_KEY:
        print(f"\n{'='*60}")
        print(f"📧 EMAIL (dev mode — no BREVO_API_KEY set)")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        if attachment:
            print(f"📎 Attachment: {attachment.get('name', 'file')}")
        print(f"{'='*60}\n")
        return True

    try:
        payload = {
            "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
            "to": [{"email": to_email}],
            "subject": subject,
            "htmlContent": html_body,
        }
        if attachment:
            payload["attachment"] = [attachment]

        response = requests.post(
            BREVO_API_URL,
            headers={
                "api-key": BREVO_API_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=payload,
            timeout=15,
        )
        if response.status_code in (200, 201):
            print(f"✅ Email sent to {to_email}: {subject}")
            return True
        else:
            print(f"❌ Email failed ({response.status_code}): {response.text}")
            return False
    except Exception as e:
        print(f"❌ Email send failed to {to_email}: {e}")
        return False


# ---------------------------------------------------------------------------
# Branded HTML wrapper
# ---------------------------------------------------------------------------
def _wrap_html(title: str, body_html: str) -> str:
    """Wrap email content in branded template."""
    return f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px;
                margin: 0 auto; background: #FEFAE0; border-radius: 16px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #D4A373, #B8864A);
                    padding: 32px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 28px;">🧁 Cream & Co.</h1>
            <p style="color: #FAEDCD; margin: 8px 0 0;">{title}</p>
        </div>
        <div style="padding: 32px;">
            {body_html}
        </div>
        <div style="background: #FAEDCD; padding: 16px; text-align: center;">
            <p style="color: #9CA3AF; font-size: 12px; margin: 0;">
                Cream & Co. | 103, Mukti Marg, Dewas | FSSAI: 21422790001224
            </p>
        </div>
    </div>
    """


# ---------------------------------------------------------------------------
# Customer Emails
# ---------------------------------------------------------------------------
def send_otp_email(to_email: str, full_name: str, otp_code: str) -> bool:
    """Send OTP verification code to new user."""
    subject = f"Your verification code: {otp_code} — Cream & Co."
    body = f"""
        <h2 style="color: #2B2B2B; margin-top: 0;">Welcome, {full_name}! 🎉</h2>
        <p style="color: #6B7280; line-height: 1.6;">
            Your verification code is:
        </p>
        <div style="text-align: center; margin: 24px 0;">
            <span style="background: #D4A373; color: white; padding: 16px 40px;
                         border-radius: 12px; font-size: 32px; font-weight: 700;
                         letter-spacing: 8px; display: inline-block;">
                {otp_code}
            </span>
        </div>
        <p style="color: #9CA3AF; font-size: 13px;">
            This code expires in 10 minutes. If you didn't create this account,
            please ignore this email.
        </p>
    """
    return _send_email(to_email, subject, _wrap_html("Email Verification", body))


def send_order_confirmation_email(
    to_email: str,
    full_name: str,
    order_number: str,
    total_amount: float,
    items_summary: str,
    items: list[dict] | None = None,
    subtotal: float = 0.0,
    delivery_fee: float = 0.0,
    delivery_address: str = "",
) -> bool:
    """Send order confirmation with PDF invoice attached."""
    subject = f"Order Confirmed — {order_number} | Cream & Co."
    body = f"""
        <h2 style="color: #2B2B2B; margin-top: 0;">Thank you, {full_name}! 🎂</h2>
        <div style="background: white; border-radius: 12px; padding: 20px; margin: 16px 0;">
            <p style="margin: 4px 0; color: #6B7280;"><strong>Order #:</strong> {order_number}</p>
            <p style="margin: 4px 0; color: #6B7280;"><strong>Total:</strong> ₹{total_amount:.2f}</p>
            <hr style="border: none; border-top: 1px solid #E5E7EB; margin: 12px 0;">
            <p style="margin: 4px 0; color: #6B7280; font-size: 14px;">{items_summary}</p>
        </div>
        <p style="color: #6B7280; line-height: 1.6;">
            Your order is being prepared with love. We'll notify you when it's
            ready for delivery!
        </p>
        <p style="color: #9CA3AF; font-size: 12px; margin-top: 16px;">
            📎 Your invoice is attached as a PDF.
        </p>
    """

    # Generate PDF invoice attachment
    attachment = None
    if items:
        try:
            from .pdf_service import generate_invoice_pdf_base64
            pdf_b64 = generate_invoice_pdf_base64(
                order_number=order_number,
                customer_name=full_name,
                delivery_address=delivery_address,
                items=items,
                subtotal=subtotal or total_amount,
                delivery_fee=delivery_fee,
                total_amount=total_amount,
            )
            attachment = {
                "content": pdf_b64,
                "name": f"Invoice_{order_number}.pdf",
            }
        except Exception as e:
            print(f"⚠️ PDF generation failed, sending without invoice: {e}")

    return _send_email(
        to_email, subject,
        _wrap_html("Order Confirmed!", body),
        attachment=attachment,
    )


def send_order_cancelled_email(
    to_email: str, full_name: str, order_number: str,
) -> bool:
    """Notify customer their order was cancelled."""
    subject = f"Order Cancelled — {order_number} | Cream & Co."
    body = f"""
        <h2 style="color: #2B2B2B; margin-top: 0;">Order Cancelled</h2>
        <p style="color: #6B7280; line-height: 1.6;">
            Hi {full_name}, your order <strong>{order_number}</strong> has been cancelled.
        </p>
        <p style="color: #9CA3AF; font-size: 13px;">
            If you didn't request this, please contact us.
        </p>
    """
    return _send_email(to_email, subject, _wrap_html("Order Cancelled", body))


def send_order_status_email(
    to_email: str, full_name: str, order_number: str, new_status: str,
) -> bool:
    """Notify customer when their order status is updated by admin."""
    status_info = {
        "confirmed": {
            "emoji": "✅",
            "title": "Order Confirmed",
            "message": "Your order has been confirmed and will be prepared shortly.",
        },
        "preparing": {
            "emoji": "👨‍🍳",
            "title": "Being Prepared",
            "message": "Our team is preparing your order with love!",
        },
        "out_for_delivery": {
            "emoji": "🚚",
            "title": "Out for Delivery",
            "message": "Your order is on its way! Please be ready to receive it.",
        },
        "delivered": {
            "emoji": "📦",
            "title": "Delivered",
            "message": "Your order has been delivered. Enjoy! 🎉",
        },
        "cancelled": {
            "emoji": "❌",
            "title": "Cancelled",
            "message": "Your order has been cancelled. Contact us if you have questions.",
        },
    }

    info = status_info.get(new_status)
    if not info:
        return False

    subject = f"{info['emoji']} Order {info['title']} — {order_number} | Cream & Co."
    body = f"""
        <h2 style="color: #2B2B2B; margin-top: 0;">
            {info['emoji']} {info['title']}
        </h2>
        <div style="background: white; border-radius: 12px; padding: 20px; margin: 16px 0;">
            <p style="margin: 4px 0; color: #6B7280;">
                <strong>Order:</strong> {order_number}
            </p>
            <p style="margin: 4px 0; color: #6B7280;">
                <strong>Status:</strong> {new_status.replace('_', ' ').title()}
            </p>
        </div>
        <p style="color: #6B7280; line-height: 1.6;">
            Hi {full_name}, {info['message']}
        </p>
        <div style="text-align: center; margin-top: 24px;">
            <a href="{APP_BASE_URL}/account/orders"
               style="background: #D4A373; color: white; padding: 12px 28px;
                      border-radius: 12px; text-decoration: none; font-weight: 600;
                      display: inline-block;">
                View My Orders
            </a>
        </div>
    """
    return _send_email(to_email, subject, _wrap_html(info['title'], body))


def send_password_reset_email(to_email: str, full_name: str, token: str) -> bool:
    """Send password reset link."""
    reset_url = f"{APP_BASE_URL}/reset-password?token={token}"
    subject = "Reset your Cream & Co. password"
    body = f"""
        <h2 style="color: #2B2B2B; margin-top: 0;">Password Reset</h2>
        <p style="color: #6B7280; line-height: 1.6;">
            Hi {full_name}, click the button below to set a new password.
        </p>
        <div style="text-align: center; margin: 32px 0;">
            <a href="{reset_url}"
               style="background: #D4A373; color: white; padding: 14px 32px;
                      border-radius: 12px; text-decoration: none; font-weight: 600;
                      font-size: 16px; display: inline-block;">
                Reset Password
            </a>
        </div>
        <p style="color: #9CA3AF; font-size: 13px;">
            This link expires in 1 hour. If you didn't request this, ignore this email.
        </p>
    """
    return _send_email(to_email, subject, _wrap_html("Password Reset", body))


# ---------------------------------------------------------------------------
# Owner Notification Emails
# ---------------------------------------------------------------------------
def _send_owner_email(subject: str, body_html: str) -> bool:
    """Send notification to shop owner."""
    if not OWNER_EMAIL:
        print("⚠️ OWNER_NOTIFICATION_EMAIL not set, skipping.")
        return False
    wrapped = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px;
                margin: 0 auto; background: #FEFAE0; border-radius: 16px; overflow: hidden;">
        <div style="background: linear-gradient(135deg, #E63946, #C1121F);
                    padding: 32px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 24px;">🔔 Admin Notification</h1>
            <p style="color: #FFD6D9; margin: 8px 0 0;">Cream & Co.</p>
        </div>
        <div style="padding: 32px;">{body_html}</div>
    </div>
    """
    return _send_email(OWNER_EMAIL, subject, wrapped)


def notify_owner_new_signup(customer_name: str, customer_email: str) -> bool:
    """Notify owner of a new customer signup."""
    return _send_owner_email(
        f"👤 New Signup: {customer_name}",
        f"""<h2 style="color:#2B2B2B;margin-top:0;">New Customer Registered</h2>
            <div style="background:white;border-radius:12px;padding:20px;">
                <p style="margin:4px 0;color:#6B7280;"><strong>Name:</strong> {customer_name}</p>
                <p style="margin:4px 0;color:#6B7280;"><strong>Email:</strong> {customer_email}</p>
            </div>"""
    )


def notify_owner_new_order(
    customer_name: str, customer_email: str, customer_phone: str,
    order_number: str, total_amount: float, items_summary: str,
    delivery_address: str, payment_method: str,
) -> bool:
    """Notify owner of a new order."""
    return _send_owner_email(
        f"🛒 New Order! {order_number} — ₹{total_amount:.2f}",
        f"""<h2 style="color:#2B2B2B;margin-top:0;">Order {order_number}</h2>
            <div style="background:white;border-radius:12px;padding:20px;margin:12px 0;">
                <p style="margin:4px 0;color:#6B7280;"><strong>Items:</strong> {items_summary}</p>
                <p style="margin:4px 0;color:#6B7280;"><strong>Total:</strong> ₹{total_amount:.2f}</p>
                <p style="margin:4px 0;color:#6B7280;"><strong>Payment:</strong> {payment_method.upper()}</p>
            </div>
            <div style="background:white;border-radius:12px;padding:20px;margin:12px 0;">
                <p style="margin:4px 0;color:#6B7280;"><strong>Customer:</strong> {customer_name}</p>
                <p style="margin:4px 0;color:#6B7280;"><strong>Email:</strong> {customer_email}</p>
                <p style="margin:4px 0;color:#6B7280;"><strong>Phone:</strong> {customer_phone}</p>
                <p style="margin:4px 0;color:#6B7280;"><strong>Address:</strong> {delivery_address}</p>
            </div>
            <div style="text-align:center;margin-top:20px;">
                <a href="{APP_BASE_URL}/admin/orders"
                   style="background:#D4A373;color:white;padding:12px 28px;border-radius:12px;
                          text-decoration:none;font-weight:600;display:inline-block;">
                    View in Admin Panel
                </a>
            </div>"""
    )


def notify_owner_order_cancelled(
    customer_name: str, order_number: str, total_amount: float,
) -> bool:
    """Notify owner of a cancelled order."""
    return _send_owner_email(
        f"❌ Order Cancelled: {order_number}",
        f"""<h2 style="color:#2B2B2B;margin-top:0;">Order Cancelled</h2>
            <div style="background:white;border-radius:12px;padding:20px;">
                <p style="margin:4px 0;color:#6B7280;"><strong>Order:</strong> {order_number}</p>
                <p style="margin:4px 0;color:#6B7280;"><strong>Customer:</strong> {customer_name}</p>
                <p style="margin:4px 0;color:#6B7280;"><strong>Amount:</strong> ₹{total_amount:.2f}</p>
            </div>"""
    )
