"""
Cream & Co. — Authentication Service
======================================
Handles password hashing, JWT token generation/validation.
"""

import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional


# ---------------------------------------------------------------------------
# Configuration from environment
# ---------------------------------------------------------------------------
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRY_DAYS = int(os.getenv("JWT_EXPIRY_DAYS", "7"))


# ---------------------------------------------------------------------------
# Password Utilities
# ---------------------------------------------------------------------------
def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt with 12 salt rounds."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ---------------------------------------------------------------------------
# JWT Token Utilities
# ---------------------------------------------------------------------------
def create_access_token(
    user_id: str,
    email: str,
    is_admin: bool = False,
    full_name: str = "",
) -> str:
    """
    Generate a signed JWT access token.

    Payload includes user_id, email, admin status, and expiry.
    """
    payload = {
        "user_id": user_id,
        "email": email,
        "is_admin": is_admin,
        "full_name": full_name,
        "exp": datetime.utcnow() + timedelta(days=JWT_EXPIRY_DAYS),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.

    Returns the payload dict on success, None if expired or invalid.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
