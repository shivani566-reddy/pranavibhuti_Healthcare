# app/models/health_locker.py
"""
Health Locker tables — stores metadata for documents in AWS S3.
Actual files are in S3; only the URL and metadata are in PostgreSQL.
"""
import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin


class DocumentType(str, enum.Enum):
    PRESCRIPTION        = "prescription"
    LAB_REPORT          = "lab_report"
    VACCINATION         = "vaccination"
    CONSULTATION_RECORD = "consultation_record"
    SCAN                = "scan"
    OTHER               = "other"


class HealthRecord(TimestampMixin, Base):
    __tablename__ = "health_records"

    id            = Column(Integer, primary_key=True, index=True)
    patient_id    = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    document_type = Column(SAEnum(DocumentType), nullable=False)
    title         = Column(String(300), nullable=False)
    description   = Column(Text)
    file_url      = Column(String(500), nullable=False)   # S3 URL
    file_name     = Column(String(300))
    file_size_kb  = Column(Integer)
    is_shared     = Column(Boolean, default=False)   # shared with doctor?
    shared_with   = Column(Integer, ForeignKey("doctors.id"), nullable=True)

    patient = relationship("User", foreign_keys=[patient_id])
