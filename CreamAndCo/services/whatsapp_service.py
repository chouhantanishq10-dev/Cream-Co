"""
Cream & Co. — WhatsApp Notification Service
=============================================
Sends OTP codes and order status updates via the official
Meta Cloud API (WhatsApp Business Platform).

Pricing (India, as of 2024):
  - Authentication (OTP): ~₹0.11 / message
  - Utility (order updates): ~₹0.30 / message
  - 1,000 free service conversations/month

Setup:
  1. Create a Meta Business account + Meta App at https://developers.facebook.com
  2. Enable WhatsApp product → Get a test phone number
  3. Create message templates (must be approved by Meta):
       - "otp_code" (category: Authentication)
       - "order_update" (category: Utility)
  4. Generate a permanent access token
  5. Add to .env:
       WHATSAPP_TOKEN=your-token
       WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
       WHATSAPP_ENABLED=true
"""

import os
import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_ENABLED = os.getenv("WHATSAPP_ENABLED", "false").lower() == "true"

GRAPH_API_URL = "https://graph.facebook.com/v21.0"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _format_phone(phone: str) -> str:
    """
    Normalize phone to international format without '+'.
    Assumes Indian numbers if 10 digits.
    """
    clean = "".join(ch for ch in phone if ch.isdigit())
    if len(clean) == 10:
        return f"91{clean}"
    return clean


def _send_template(
    to_phone: str,
    template_name: str,
    components: list[dict],
    language: str = "en",
) -> bool:
    """
    Low-level sender: dispatches a pre-approved WhatsApp template.
    Returns True on success.
    """
    if not WHATSAPP_ENABLED:
        return True  # silently skip when not configured

    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print("⚠️  WhatsApp credentials missing (WHATSAPP_TOKEN / PHONE_NUMBER_ID)")
        return False

    url = f"{GRAPH_API_URL}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": _format_phone(to_phone),
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language},
            "components": components,
        },
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        if resp.status_code in (200, 201):
            print(f"✅ WhatsApp sent '{template_name}' to {to_phone}")
            return True
        print(f"❌ WhatsApp error ({resp.status_code}): {resp.text}")
        return False
    except Exception as e:
        print(f"❌ WhatsApp exception: {e}")
        return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def send_whatsapp_otp(phone: str, otp_code: str) -> bool:
    """
    Send OTP verification code via WhatsApp.

    Requires a Meta-approved template named "otp_code" (Authentication category)
    with one body parameter: {{1}} = the OTP code.
    """
    if not phone:
        return False
    return _send_template(
        to_phone=phone,
        template_name="otp_code",
        components=[
            {
                "type": "body",
                "parameters": [{"type": "text", "text": otp_code}],
            }
        ],
    )


def send_whatsapp_order_status(
    phone: str,
    order_number: str,
    status_message: str,
) -> bool:
    """
    Send order status update via WhatsApp.

    Requires a Meta-approved template named "order_update" (Utility category)
    with two body parameters:
      {{1}} = order number
      {{2}} = human-readable status message
    """
    if not phone:
        return False

    return _send_template(
        to_phone=phone,
        template_name="order_update",
        components=[
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": order_number},
                    {"type": "text", "text": status_message},
                ],
            }
        ],
    )
