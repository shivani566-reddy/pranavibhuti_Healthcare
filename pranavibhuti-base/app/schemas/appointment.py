# app/schemas/appointment.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.appointment import AppointmentStatus


class AppointmentCreate(BaseModel):
    doctor_id: int
    slot_id: int
    reason: Optional[str] = None


class AppointmentCancel(BaseModel):
    cancel_reason: Optional[str] = None


class AppointmentReschedule(BaseModel):
    new_slot_id: int


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    slot_id: int
    status: AppointmentStatus
    reason: Optional[str] = None
    notes: Optional[str] = None
    booked_at: datetime
    cancelled_at: Optional[datetime] = None
    cancel_reason: Optional[str] = None
    completed_at: Optional[datetime] = None
    model_config = {"from_attributes": True}
