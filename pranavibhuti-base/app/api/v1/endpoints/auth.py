# app/api/v1/endpoints/auth.py
"""
Authentication endpoints — owned by Member 4 (Auth lead).

POST /api/v1/auth/register   → register new user
POST /api/v1/auth/login      → login, get tokens
POST /api/v1/auth/verify-otp → verify OTP, activate account
POST /api/v1/auth/refresh    → get new access token using refresh token
GET  /api/v1/auth/me         → get current logged-in user's info
POST /api/v1/auth/logout     → logout (client discards token)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, OTPVerify, UserResponse, UserUpdate
from app.schemas.common import TokenResponse
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, verify_token
from app.core.dependencies import get_current_user
from app.core.response import success_response, error_response
import random, string
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    """Register a new patient, doctor, or admin account."""

    # Check duplicate email
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered.")

    # Check duplicate phone
    existing_phone = await db.execute(select(User).where(User.phone == data.phone))
    if existing_phone.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Phone number already registered.")

    # Generate OTP
    otp = "".join(random.choices(string.digits, k=6))
    otp_expires = (datetime.utcnow() + timedelta(minutes=10)).isoformat()

    user = User(
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        hashed_password=hash_password(data.password),
        role=data.role,
        otp_code=otp,
        otp_expires_at=otp_expires,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    # TODO (Phase 1): Send OTP via SMS/email using notification service
    # For now, return OTP in response (remove in production)
    return success_response(
        "Registration successful. Verify your account with the OTP sent to your phone/email.",
        {"user_id": user.id, "otp_for_testing": otp},
        status_code=201,
    )


@router.post("/verify-otp")
async def verify_otp(data: OTPVerify, db: AsyncSession = Depends(get_db)):
    """Verify OTP and activate the account."""
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.is_verified:
        return success_response("Account already verified.")
    if user.otp_code != data.otp_code:
        raise HTTPException(status_code=400, detail="Invalid OTP.")
    if datetime.utcnow() > datetime.fromisoformat(user.otp_expires_at):
        raise HTTPException(status_code=400, detail="OTP expired. Please register again.")

    user.is_verified = True
    user.otp_code = None
    user.otp_expires_at = None
    return success_response("Account verified successfully.")


@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login and receive access + refresh tokens."""
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated.")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your account first.")

    access_token = create_access_token(user.id, user.role.value)
    refresh_token = create_refresh_token(user.id, user.role.value)

    return success_response("Login successful.", {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role.value,
        "user_id": user.id,
        "full_name": user.full_name,
    })


@router.post("/refresh")
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """Get a new access token using a valid refresh token."""
    from jose import JWTError
    try:
        payload = verify_token(refresh_token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token.")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Provide a refresh token.")

    new_access = create_access_token(int(payload["sub"]), payload["role"])
    return success_response("Token refreshed.", {"access_token": new_access, "token_type": "bearer"})


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Get the currently logged-in user's profile."""
    result = await db.execute(select(User).where(User.id == int(current_user["sub"])))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return success_response("User profile fetched.", UserResponse.model_validate(user).model_dump())


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout — client must discard the token.
    Phase 3: implement token blacklist in Redis.
    """
    return success_response("Logged out successfully.")
