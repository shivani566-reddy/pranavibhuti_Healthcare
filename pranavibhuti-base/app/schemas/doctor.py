# app/schemas/doctor.py
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import date, time, datetime


class DoctorCreate(BaseModel):
    name: str
    email: str
    phone: str
    specialization: str
    qualification: str
    hospital_name: Optional[str] = None
    hospital_address: Optional[str] = None
    experience_years: Optional[int] = 0
    consultation_fee: Optional[float] = 0.0
    bio: Optional[str] = None
    profile_picture: Optional[str] = None


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    qualification: Optional[str] = None
    hospital_name: Optional[str] = None
    hospital_address: Optional[str] = None
    experience_years: Optional[int] = None
    consultation_fee: Optional[float] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None


class DoctorResponse(BaseModel):
    id: int
    user_id: int
    name: str
    email: str
    phone: str
    specialization: str
    qualification: str
    hospital_name: Optional[str] = None
    hospital_address: Optional[str] = None
    experience_years: int
    consultation_fee: float
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    rating: float
    total_reviews: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    model_config = {"from_attributes": True}


class SlotCreate(BaseModel):
    slot_date: date
    start_time: time
    end_time: time

    @field_validator("end_time")
    @classmethod
    def end_after_start(cls, v, info):
        if "start_time" in info.data and v <= info.data["start_time"]:
            raise ValueError("end_time must be after start_time")
        return v


class SlotBulkCreate(BaseModel):
    slots: List[SlotCreate]


class SlotResponse(BaseModel):
    id: int
    doctor_id: int
    slot_date: date
    start_time: time
    end_time: time
    is_booked: bool
    is_blocked: bool
    model_config = {"from_attributes": True}
