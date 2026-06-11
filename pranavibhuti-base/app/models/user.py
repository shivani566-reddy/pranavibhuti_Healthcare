# app/models/user.py
"""
Users table — owned by Member 4 (Auth lead).
ALL other teams reference this table via foreign keys.

Roles:
    patient  → can book appointments, order medicine, upload records
    doctor   → can manage availability, view appointments, write notes
    admin    → full access to everything
"""
import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum as SAEnum
from app.db.base import Base, TimestampMixin


class UserRole(str, enum.Enum):
    PATIENT = "patient"
    DOCTOR  = "doctor"
    ADMIN   = "admin"


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id             = Column(Integer, primary_key=True, index=True)
    full_name      = Column(String(150), nullable=False)
    email          = Column(String(255), unique=True, nullable=False, index=True)
    phone          = Column(String(20), unique=True, nullable=False)
    hashed_password= Column(String(255), nullable=False)
    role           = Column(SAEnum(UserRole), nullable=False, default=UserRole.PATIENT)
    is_active      = Column(Boolean, default=True)
    is_verified    = Column(Boolean, default=False)   # OTP verified
    otp_code       = Column(String(6), nullable=True)
    otp_expires_at = Column(String(50), nullable=True)
