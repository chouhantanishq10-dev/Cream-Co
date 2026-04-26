"""
Cream & Co. — Application Constants
=====================================
Centralized constants for colors, business info, and configuration.
"""

# ---------------------------------------------------------------------------
# Brand Colors
# ---------------------------------------------------------------------------
COLORS = {
    "primary": "#D4A373",
    "primary_dark": "#B8864A",
    "primary_light": "#E8C9A0",
    "secondary": "#FAEDCD",
    "accent": "#E63946",
    "background": "#FEFAE0",
    "surface": "#FFFFFF",
    "surface_alt": "#FFF8F0",
    "text_primary": "#2B2B2B",
    "text_secondary": "#6B7280",
    "text_muted": "#9CA3AF",
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "border": "#E5E7EB",
    "border_light": "#F3F4F6",
    "gradient_start": "#D4A373",
    "gradient_end": "#B8864A",
}

# ---------------------------------------------------------------------------
# Business Information
# ---------------------------------------------------------------------------
BUSINESS = {
    "name": "Cream & Co.",
    "tagline": "Freshly Baked Happiness, Delivered!",
    "address": "103, Mukti Marg, Dewas Locality, Dewas, Madhya Pradesh, India",
    "phone": "+91 9111414565",
    "fssai": "21422790001224",
    "rating": 4.0,
    "total_ratings": 290,
    "delivery_area": "Dewas",
    "email": "hello@creamandco.in",
}

# ---------------------------------------------------------------------------
# Order Status Configuration
# ---------------------------------------------------------------------------
ORDER_STATUSES = {
    "pending": {"label": "Pending", "color": "#F59E0B", "icon": "clock"},
    "confirmed": {"label": "Confirmed", "color": "#3B82F6", "icon": "circle-check"},
    "preparing": {"label": "Preparing", "color": "#8B5CF6", "icon": "chef-hat"},
    "out_for_delivery": {"label": "Out for Delivery", "color": "#06B6D4", "icon": "truck"},
    "delivered": {"label": "Delivered", "color": "#10B981", "icon": "package-check"},
    "cancelled": {"label": "Cancelled", "color": "#EF4444", "icon": "circle-x"},
}

# Delivery fee in INR
DELIVERY_FEE = 30.0
FREE_DELIVERY_THRESHOLD = 500.0
