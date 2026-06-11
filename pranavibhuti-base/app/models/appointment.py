# app/models/appointment.py
"""
Appointments table — owned by Sreeja.
"""
import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class AppointmentStatus(str, enum.Enum):
    PENDING     = "pending"
    CONFIRMED   = "confirmed"
    CANCELLED   = "cancelled"
    COMPLETED   = "completed"
    RESCHEDULED = "rescheduled"


class Appointment(Base):
    __tablename__ = "appointments"

    id            = Column(Integer, primary_key=True, index=True)
    patient_id    = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    doctor_id     = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    slot_id       = Column(Integer, ForeignKey("doctor_slots.id"), nullable=False)
    status        = Column(SAEnum(AppointmentStatus), default=AppointmentStatus.PENDING, nullable=False)
    reason        = Column(Text)
    notes         = Column(Text)
    booked_at     = Column(DateTime, default=datetime.utcnow)
    cancelled_at  = Column(DateTime, nullable=True)
    cancel_reason = Column(String(500), nullable=True)
    completed_at  = Column(DateTime, nullable=True)

    doctor  = relationship("Doctor", back_populates="appointments")
    slot    = relationship("DoctorSlot")
    patient = relationship("User", foreign_keys=[patient_id])
