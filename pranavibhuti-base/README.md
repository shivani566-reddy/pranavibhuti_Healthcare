# PRANAVIBHUTI — Base Project

Complete healthcare platform backend. FastAPI + PostgreSQL + SQLAlchemy (async).

---

## Team Ownership

| Module | Owner | Files |
|---|---|---|
| Auth / Users | Member 4 | `app/api/v1/endpoints/auth.py`, `app/models/user.py` |
| Doctors / Appointments / Notifications | Sreeja | `app/api/v1/endpoints/doctors.py`, `appointments.py` |
| Pharmacy / Lab | Vaishnavi | `app/api/v1/endpoints/pharmacy.py`, `lab.py` *(create these)* |
| AI / Telemedicine | Nethaji | `app/api/v1/endpoints/ai.py`, `telemedicine.py` *(create these)* |
| Admin Panel | Akhil Reddy | `app/api/v1/endpoints/admin.py` *(create this)* |
| DevOps / Infra | Shiva kiran | `Dockerfile`, deployment config |
| Database | Member 8 | `migrations/schema.sql` |

---

## Run for everyone (any machine)

```bash
# 1. Clone
git clone <repo-url>
cd pranavibhuti-base

# 2. Virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
# Edit .env — fill DATABASE_URL and JWT_SECRET_KEY

# 5. Create database (in psql or pgAdmin)
CREATE DATABASE pranavibhuti;

# 6. Start server (tables auto-created)
uvicorn app.main:app --reload

# 7. Seed sample data (optional, first time only)
python scripts/seed.py

# 8. Open docs
open http://localhost:8000/docs
```

---

## How to add your module

**Step 1** — Create your endpoint file:
```
app/api/v1/endpoints/pharmacy.py
```

**Step 2** — Register it in the master router:
```python
# app/api/v1/router.py
from app.api.v1.endpoints.pharmacy import router as pharmacy_router
api_router.include_router(pharmacy_router)
```

**Step 3** — If you add a new model, import it in:
```
app/models/__init__.py
```

That's it. Your routes appear in Swagger automatically.

---

## Standard response format (ALL responses must use this)

```json
{
    "success": true,
    "message": "Appointment booked.",
    "data": { ... }
}
```

Use the helpers:
```python
from app.core.response import success_response, error_response

return success_response("Doctor fetched.", doctor_data)
return error_response("Slot not available.", status_code=409)
```

---

## RBAC — How security works

```python
from app.core.dependencies import require_patient, require_doctor, assert_owner

# Only patients can call this:
@router.post("/appointments")
async def book(current_user: dict = Depends(require_patient)):
    patient_id = int(current_user["sub"])   # always from JWT

# Row-level: patient can only cancel their own appointment:
assert_owner(appointment.patient_id, current_user, "appointment")
```

Never trust `user_id` from the request body. Always use `int(current_user["sub"])`.

---

## JWT payload (all team members must know this)

```json
{
  "sub": "123",
  "role": "patient",
  "type": "access",
  "iat": 1234567890,
  "exp": 1234567890
}
```

Roles: `patient` | `doctor` | `admin`

---

## API base URLs

```
Auth:         /api/v1/auth/*
Doctors:      /api/v1/doctors/*
Appointments: /api/v1/appointments/*
Pharmacy:     /api/v1/pharmacy/*        ← Vaishnavi adds this
Lab:          /api/v1/lab/*             ← Vaishnavi adds this
AI:           /api/v1/ai/*              ← Nethaji adds this
Admin:        /api/v1/admin/*           ← Akhil adds this
Health Locker:/api/v1/health-locker/*   ← Phase 3
```

---

## Run tests

```bash
pytest tests/
```

---

## Environment variables (ask team lead for values)

| Variable | Who sets it |
|---|---|
| `DATABASE_URL` | Each person uses their own local PostgreSQL |
| `JWT_SECRET_KEY` | Member 4 sets it — ALL members must use the SAME value |
| Everything else | Leave blank for Phase 1 |

---

## Phase roadmap

| Phase | Focus |
|---|---|
| Phase 1 | Auth, Doctors, Appointments, Notification skeleton, RBAC ✅ |
| Phase 2 | Admin, Pharmacy, Lab, Profile management |
| Phase 3 | Telemedicine, AI, Payments, Real notifications, Health Locker |
