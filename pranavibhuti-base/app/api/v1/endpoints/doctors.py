# app/api/v1/endpoints/doctors.py
"""
Doctor endpoints — owned by Sreeja.

PUBLIC (no auth needed):
  GET  /api/v1/doctors                          → list all doctors
  GET  /api/v1/doctors/search?specialization=  → search by specialization
  GET  /api/v1/doctors/{id}                    → get doctor profile
  GET  /api/v1/doctors/{id}/slots              → get available slots

DOCTOR ONLY:
  POST   /api/v1/doctors                       → create my profile
  GET    /api/v1/doctors/me                    → get my profile
  PATCH  /api/v1/doctors/{id}                  → update my profile (RBAC)
  POST   /api/v1/doctors/{id}/slots            → add my slots (RBAC)
  PATCH  /api/v1/doctors/{id}/slots/{sid}/block → block/unblock slot (RBAC)
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime
from app.db.session import get_db
from app.models.doctor import Doctor, DoctorSlot
from app.schemas.doctor import (
    DoctorCreate, DoctorUpdate, DoctorResponse,
    SlotBulkCreate, SlotResponse
)
from app.core.dependencies import require_doctor, get_current_user, assert_owner
from app.core.response import success_response

router = APIRouter(prefix="/doctors", tags=["Doctors"])


# ── Public ─────────────────────────────────────────────────────────────────────

@router.get("")
async def list_doctors(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Doctor).where(Doctor.is_active == True).offset(skip).limit(limit)
    )
    doctors = result.scalars().all()
    return success_response("Doctors fetched.", [DoctorResponse.model_validate(d).model_dump() for d in doctors])


@router.get("/search")
async def search_doctors(
    specialization: str = Query(..., min_length=2),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Doctor)
        .where(Doctor.specialization.ilike(f"%{specialization}%"), Doctor.is_active == True)
        .offset(skip).limit(limit)
    )
    doctors = result.scalars().all()
    return success_response("Search results.", [DoctorResponse.model_validate(d).model_dump() for d in doctors])


@router.get("/me")
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_doctor),
):
    result = await db.execute(select(Doctor).where(Doctor.user_id == int(current_user["sub"])))
    doctor = result.scalar_one_or_none()
    if not doctor:
        raise HTTPException(404, "Doctor profile not found. Create your profile first.")
    return success_response("Profile fetched.", DoctorResponse.model_validate(doctor).model_dump())


@router.get("/{doctor_id}")
async def get_doctor(doctor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id, Doctor.is_active == True))
    doctor = result.scalar_one_or_none()
    if not doctor:
        raise HTTPException(404, "Doctor not found.")
    return success_response("Doctor fetched.", DoctorResponse.model_validate(doctor).model_dump())


@router.get("/{doctor_id}/slots")
async def get_slots(
    doctor_id: int,
    available_only: bool = Query(True),
    db: AsyncSession = Depends(get_db),
):
    query = select(DoctorSlot).where(DoctorSlot.doctor_id == doctor_id)
    if available_only:
        query = query.where(DoctorSlot.is_booked == False, DoctorSlot.is_blocked == False)
    result = await db.execute(query.order_by(DoctorSlot.slot_date, DoctorSlot.start_time))
    slots = result.scalars().all()
    return success_response("Slots fetched.", [SlotResponse.model_validate(s).model_dump() for s in slots])


# ── Doctor auth required ───────────────────────────────────────────────────────

@router.post("", status_code=201)
async def create_profile(
    data: DoctorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_doctor),
):
    user_id = int(current_user["sub"])
    existing = await db.execute(select(Doctor).where(Doctor.user_id == user_id))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Doctor profile already exists.")
    doctor = Doctor(user_id=user_id, **data.model_dump())
    db.add(doctor)
    await db.flush()
    await db.refresh(doctor)
    return success_response("Profile created.", DoctorResponse.model_validate(doctor).model_dump(), 201)


@router.patch("/{doctor_id}")
async def update_profile(
    doctor_id: int,
    data: DoctorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_doctor),
):
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar_one_or_none()
    if not doctor:
        raise HTTPException(404, "Doctor not found.")
    assert_owner(doctor.user_id, current_user, "doctor profile")   # RBAC
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(doctor, field, value)
    doctor.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(doctor)
    return success_response("Profile updated.", DoctorResponse.model_validate(doctor).model_dump())


@router.post("/{doctor_id}/slots", status_code=201)
async def add_slots(
    doctor_id: int,
    data: SlotBulkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_doctor),
):
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar_one_or_none()
    if not doctor:
        raise HTTPException(404, "Doctor not found.")
    assert_owner(doctor.user_id, current_user, "doctor slots")   # RBAC
    slots = [DoctorSlot(doctor_id=doctor_id, **s.model_dump()) for s in data.slots]
    for slot in slots:
        db.add(slot)
    await db.flush()
    return success_response("Slots added.", [SlotResponse.model_validate(s).model_dump() for s in slots], 201)


@router.patch("/{doctor_id}/slots/{slot_id}/block")
async def toggle_block_slot(
    doctor_id: int,
    slot_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_doctor),
):
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doctor = result.scalar_one_or_none()
    if not doctor:
        raise HTTPException(404, "Doctor not found.")
    assert_owner(doctor.user_id, current_user, "doctor slots")   # RBAC
    slot_result = await db.execute(
        select(DoctorSlot).where(DoctorSlot.id == slot_id, DoctorSlot.doctor_id == doctor_id)
    )
    slot = slot_result.scalar_one_or_none()
    if not slot:
        raise HTTPException(404, "Slot not found.")
    if slot.is_booked:
        raise HTTPException(400, "Cannot block a booked slot.")
    slot.is_blocked = not slot.is_blocked
    await db.flush()
    await db.refresh(slot)
    action = "blocked" if slot.is_blocked else "unblocked"
    return success_response(f"Slot {action}.", SlotResponse.model_validate(slot).model_dump())
