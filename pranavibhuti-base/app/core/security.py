# app/core/security.py
"""
Security utilities — JWT creation/verification and password hashing.

ALL team members use these functions.
DO NOT create your own JWT logic — import from here.

Usage:
    from app.core.security import (
        create_access_token,
        create_refresh_token,
        verify_token,
        hash_password,
        verify_password,
    )
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Hash a plain password before storing in DB."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plain password against the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_id: int,
    role: str,
    extra_claims: dict = None,
) -> str:
    """
    Create a short-lived access token.

    Payload structure (ALL team members must read this):
    {
        "sub": "123",          ← user_id as string
        "role": "doctor",      ← "patient" | "doctor" | "admin"
        "type": "access",
        "exp": <timestamp>,
        "iat": <timestamp>,
        ... any extra_claims
    }
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: int, role: str) -> str:
    """Create a long-lived refresh token."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def verify_token(token: str) -> dict:
    """
    Decode and validate a JWT token.
    Returns the payload dict on success.
    Raises JWTError on failure (handled by auth middleware).
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError as e:
        raise e
