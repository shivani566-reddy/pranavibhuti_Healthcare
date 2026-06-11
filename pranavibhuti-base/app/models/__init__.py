# app/models/__init__.py
"""
Import ALL models here so SQLAlchemy and Alembic discover them.
Every team member must add their model import here when they create a new model.
"""
from app.models.user import User, UserRole
from app.models.doctor import Doctor, DoctorSlot
from app.models.appointment import Appointment, AppointmentStatus
from app.models.pharmacy import Medicine, MedicineOrder, MedicineOrderItem, OrderStatus
from app.models.lab import LabTest, LabBooking, LabBookingStatus
from app.models.notification import NotificationLog, NotificationType, NotificationStatus
from app.models.health_locker import HealthRecord, DocumentType

__all__ = [
    "User", "UserRole",
    "Doctor", "DoctorSlot",
    "Appointment", "AppointmentStatus",
    "Medicine", "MedicineOrder", "MedicineOrderItem", "OrderStatus",
    "LabTest", "LabBooking", "LabBookingStatus",
    "NotificationLog", "NotificationType", "NotificationStatus",
    "HealthRecord", "DocumentType",
]
