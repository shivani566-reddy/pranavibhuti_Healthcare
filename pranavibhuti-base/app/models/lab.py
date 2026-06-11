# app/models/lab.py
"""
Laboratory tables — owned by Vaishnavi.
"""
import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, Date, ForeignKey, DECIMAL, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class LabBookingStatus(str, enum.Enum):
    BOOKED    = "booked"
    SAMPLE_COLLECTED = "sample_collected"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class LabTest(TimestampMixin, Base):
    __tablename__ = "lab_tests"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(200), nullable=False)
    category     = Column(String(100))
    description  = Column(Text)
    price        = Column(DECIMAL(10, 2), nullable=False)
    turnaround_hours = Column(Integer, default=24)
    home_collection_available = Column(Boolean, default=True)
    is_active    = Column(Boolean, default=True)


class LabBooking(TimestampMixin, Base):
    __tablename__ = "lab_bookings"

    id               = Column(Integer, primary_key=True, index=True)
    patient_id       = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    test_id          = Column(Integer, ForeignKey("lab_tests.id"), nullable=False)
    status           = Column(SAEnum(LabBookingStatus), default=LabBookingStatus.BOOKED)
    collection_date  = Column(Date, nullable=False)
    home_collection  = Column(Boolean, default=False)
    collection_address = Column(Text)
    amount           = Column(DECIMAL(10, 2), nullable=False)
    report_url       = Column(String(500), nullable=True)
    payment_id       = Column(String(200), nullable=True)

    test    = relationship("LabTest")
    patient = relationship("User", foreign_keys=[patient_id])
