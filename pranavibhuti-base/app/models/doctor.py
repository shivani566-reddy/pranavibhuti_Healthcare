# app/models/doctor.py
"""
Doctors and DoctorSlots tables — owned by Sreeja.
"""
from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    Date, Time, ForeignKey, DECIMAL, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class Doctor(TimestampMixin, Base):
    __tablename__ = "doctors"

    id               = Column(Integer, primary_key=True, index=True)
    user_id          = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name             = Column(String(150), nullable=False)
    email            = Column(String(255), unique=True, nullable=False)
    phone            = Column(String(20), nullable=False)
    specialization   = Column(String(100), nullable=False)
    qualification    = Column(String(200), nullable=False)
    hospital_name    = Column(String(200))
    hospital_address = Column(Text)
    experience_years = Column(Integer, default=0)
    consultation_fee = Column(DECIMAL(10, 2), default=0)
    bio              = Column(Text)
    profile_picture  = Column(String(500))
    rating           = Column(DECIMAL(3, 2), default=0.0)
    total_reviews    = Column(Integer, default=0)
    is_active        = Column(Boolean, default=True)
    is_verified      = Column(Boolean, default=False)

    slots        = relationship("DoctorSlot", back_populates="doctor", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="doctor")


class DoctorSlot(Base):
    __tablename__ = "doctor_slots"
    __table_args__ = (
        UniqueConstraint("doctor_id", "slot_date", "start_time", name="uq_doctor_slot"),
    )

    id         = Column(Integer, primary_key=True, index=True)
    doctor_id  = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    slot_date  = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time   = Column(Time, nullable=False)
    is_booked  = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)

    doctor = relationship("Doctor", back_populates="slots")
