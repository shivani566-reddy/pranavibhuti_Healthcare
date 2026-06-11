# app/api/v1/endpoints/appointments.py
"""
Appointment endpoints — owned by Sreeja.

PATIENT ONLY:
  POST   /api/v1/appointments                   → book appointment
  GET    /api/v1/appointments/my                → my appointments
  PATCH  /api/v1/appointments/{id}/cancel       → cancel mine (RBAC)
  PATCH  /api/v1/appointments/{id}/reschedule   → reschedule mine (RBAC)

DOCTOR ONLY:
  GET    /api/v1/appointments/doctor/my         → my patients' appointments
  PATCH  /api/v1/appointments/{id}/complete     → mark complete (RBAC)
"""
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.db.session import get_db
from app.models.appointment import Appointment, AppointmentStatus
from app.models.doctor import Doctor, DoctorSlot
from app.schemas.appointment import (
    AppointmentCreate, AppointmentCancel,
    AppointmentReschedule, AppointmentResponse
)
from app.core.dependencies import require_patient, require_doctor, assert_owner
from app.core.response import success_response

router = APIRouter(prefix="/appointments", tags=["Appointments"])


# ── Patient routes ─────────────────────────────────────────────────────────────

@router.post("", status_code=201)
async def book_appointment(
    data: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_patient),
):
    patient_id = int(current_user["sub"])   # always from JWT — never from body

    slot_result = await db.execute(
        select(DoctorSlot).where(DoctorSlot.id == data.slot_id, DoctorSlot.doctor_id == data.doctor_id)
    )
    slot = slot_result.scalar_one_or_none()
    if not slot:
        raise HTTPException(404, "Slot not found for this doctor.")
    if slot.is_booked:
        raise HTTPException(409, "Slot already booked.")
    if slot.is_blocked:
        raise HTTPException(409, "Slot is blocked by doctor.")

    appointment = Appointment(
        patient_id=patient_id,
        doctor_id=data.doctor_id,
        slot_id=data.slot_id,
        reason=data.reason,
        status=AppointmentStatus.CONFIRMED,
    )
    slot.is_booked = True
    db.add(appointment)
    await db.flush()
    await db.refresh(appointment)
    return success_response("Appointment booked.", AppointmentResponse.model_validate(appointment).model_dump(), 201)


@router.get("/my")
async def my_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_patient),
):
    patient_id = int(current_user["sub"])
    result = await db.execute(
        select(Appointment).where(Appointment.patient_id == patient_id)
        .order_by(Appointment.booked_at.desc())
    )
    appts = result.scalars().all()
    return success_response("Appointments fetched.", [AppointmentResponse.model_validate(a).model_dump() for a in appts])


@router.patch("/{appointment_id}/cancel")
async def cancel_appointment(
    appointment_id: int,
    data: AppointmentCancel = Body(default=AppointmentCancel()),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_patient),
):
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    appt = result.scalar_one_or_none()
    if not appt:
        raise HTTPException(404, "Appointment not found.")
    assert_owner(appt.patient_id, current_user, "appointment")   # RBAC
    if appt.status == AppointmentStatus.CANCELLED:
        raise HTTPException(400, "Already cancelled.")
    if appt.status == AppointmentStatus.COMPLETED:
        raise HTTPException(400, "Cannot cancel a completed appointment.")

    slot_result = await db.execute(select(DoctorSlot).where(DoctorSlot.id == appt.slot_id))
    slot = slot_result.scalar_one_or_none()
    if slot:
        slot.is_booked = False

    appt.status = AppointmentStatus.CANCELLED
    appt.cancelled_at = datetime.utcnow()
    appt.cancel_reason = data.cancel_reason
    await db.flush()
    await db.refresh(appt)
    return success_response("Appointment cancelled.", AppointmentResponse.model_validate(appt).model_dump())


@router.patch("/{appointment_id}/reschedule")
async def reschedule_appointment(
    appointment_id: int,
    data: AppointmentReschedule,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_patient),
):
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    appt = result.scalar_one_or_none()
    if not appt:
        raise HTTPException(404, "Appointment not found.")
    assert_owner(appt.patient_id, current_user, "appointment")   # RBAC
    if appt.status in [AppointmentStatus.CANCELLED, AppointmentStatus.COMPLETED]:
        raise HTTPException(400, f"Cannot reschedule a {appt.status.value} appointment.")

    new_slot_result = await db.execute(
        select(DoctorSlot).where(DoctorSlot.id == data.new_slot_id, DoctorSlot.doctor_id == appt.doctor_id)
    )
    new_slot = new_slot_result.scalar_one_or_none()
    if not new_slot or new_slot.is_booked or new_slot.is_blocked:
        raise HTTPException(409, "New slot is not available.")

    old_slot_result = await db.execute(select(DoctorSlot).where(DoctorSlot.id == appt.slot_id))
    old_slot = old_slot_result.scalar_one_or_none()
    if old_slot:
        old_slot.is_booked = False

    new_slot.is_booked = True
    appt.slot_id = data.new_slot_id
    appt.status = AppointmentStatus.RESCHEDULED
    await db.flush()
    await db.refresh(appt)
    return success_response("Appointment rescheduled.", AppointmentResponse.model_validate(appt).model_dump())


# ── Doctor routes ──────────────────────────────────────────────────────────────

@router.get("/doctor/my")
async def doctor_appointments(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_doctor),
):
    doctor_result = await db.execute(select(Doctor).where(Doctor.user_id == int(current_user["sub"])))
    doctor = doctor_result.scalar_one_or_none()
    if not doctor:
        raise HTTPException(404, "Doctor profile not found.")
    result = await db.execute(
        select(Appointment).where(Appointment.doctor_id == doctor.id)
        .order_by(Appointment.booked_at.desc())
    )
    appts = result.scalars().all()
    return success_response("Appointments fetched.", [AppointmentResponse.model_validate(a).model_dump() for a in appts])


@router.patch("/{appointment_id}/complete")
async def complete_appointment(
    appointment_id: int,
    notes: str = Body("", embed=True),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_doctor),
):
    doctor_result = await db.execute(select(Doctor).where(Doctor.user_id == int(current_user["sub"])))
    doctor = doctor_result.scalar_one_or_none()
    if not doctor:
        raise HTTPException(404, "Doctor profile not found.")
    result = await db.execute(
        select(Appointment).where(Appointment.id == appointment_id, Appointment.doctor_id == doctor.id)
    )
    appt = result.scalar_one_or_none()
    if not appt:
        raise HTTPException(404, "Appointment not found or not yours.")
    if appt.status != AppointmentStatus.CONFIRMED:
        raise HTTPException(400, "Only confirmed appointments can be completed.")
    appt.status = AppointmentStatus.COMPLETED
    appt.completed_at = datetime.utcnow()
    appt.notes = notes
    await db.flush()
    await db.refresh(appt)
    return success_response("Appointment completed.", AppointmentResponse.model_validate(appt).model_dump())
