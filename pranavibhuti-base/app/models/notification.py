# app/models/notification.py
"""
Notification log — owned by Sreeja.
All team members can call the notification service
to log alerts; the actual sending is wired in Phase 3.
"""
import enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SAEnum
from app.db.base import Base
from datetime import datetime


class NotificationType(str, enum.Enum):
    SMS   = "sms"
    EMAIL = "email"
    PUSH  = "push"


class NotificationStatus(str, enum.Enum):
    QUEUED = "queued"
    SENT   = "sent"
    FAILED = "failed"
    STUB   = "stub_logged"   # Phase 1 — not really sent


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    type         = Column(SAEnum(NotificationType), nullable=False)
    recipient    = Column(String(255), nullable=False)
    subject      = Column(String(300))
    message      = Column(Text, nullable=False)
    status       = Column(SAEnum(NotificationStatus), default=NotificationStatus.STUB)
    error_detail = Column(Text, nullable=True)
    sent_at      = Column(DateTime, nullable=True)
    created_at   = Column(DateTime, default=datetime.utcnow)
