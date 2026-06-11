# app/schemas/user.py
"""
User schemas — owned by Member 4 (Auth lead).
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    role: UserRole = UserRole.PATIENT


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
