# app/api/v1/router.py
"""
Master API router — ALL team members register their router here.

When you build a new set of endpoints, create your file in:
    app/api/v1/endpoints/your_module.py

Then add it below:
    from app.api.v1.endpoints.your_module import router as your_router
    api_router.include_router(your_router)
"""
from fastapi import APIRouter
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.doctors import router as doctors_router
from app.api.v1.endpoints.appointments import router as appointments_router

api_router = APIRouter(prefix="/api/v1")

# ── Auth team (Member 4) ───────────────────────────────────────────────────────
api_router.include_router(auth_router)

# ── Sreeja — Doctor / Appointment / Notification ──────────────────────────────
api_router.include_router(doctors_router)
api_router.include_router(appointments_router)

# ── Vaishnavi — Pharmacy / Lab (add when ready) ───────────────────────────────
# from app.api.v1.endpoints.pharmacy import router as pharmacy_router
# from app.api.v1.endpoints.lab import router as lab_router
# api_router.include_router(pharmacy_router)
# api_router.include_router(lab_router)

# ── Nethaji — AI / Telemedicine (add when ready) ─────────────────────────────
# from app.api.v1.endpoints.ai import router as ai_router
# api_router.include_router(ai_router)

# ── Admin (add when ready) ────────────────────────────────────────────────────
# from app.api.v1.endpoints.admin import router as admin_router
# api_router.include_router(admin_router)

# ── Health Locker (add when ready) ────────────────────────────────────────────
# from app.api.v1.endpoints.health_locker import router as locker_router
# api_router.include_router(locker_router)
