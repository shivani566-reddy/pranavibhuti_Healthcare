# scripts/seed.py
"""
Seed script — inserts sample data for development and testing.
Run once after setting up the database:
    python scripts/seed.py

Creates:
  - 1 admin user
  - 2 doctor users + doctor profiles
  - 2 patient users
  - Sample availability slots for each doctor

Credentials after seeding:
  Admin:   admin@pranavibhuti.com   / Admin@123
  Doctor1: doctor1@pranavibhuti.com / Doctor@123
  Doctor2: doctor2@pranavibhuti.com / Doctor@123
  Patient1:patient1@pranavibhuti.com / Patient@123
  Patient2:patient2@pranavibhuti.com / Patient@123
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from datetime import date, time, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal, engine
from app.db.base import Base
from app.models.user import User, UserRole
from app.models.doctor import Doctor, DoctorSlot
from app.models import *  # noqa — register all models
from app.core.security import hash_password


SAMPLE_USERS = [
    {"full_name": "Admin User",    "email": "admin@pranavibhuti.com",    "phone": "9000000001", "password": "Admin@123",   "role": UserRole.ADMIN},
    {"full_name": "Dr. Ravi Kumar","email": "doctor1@pranavibhuti.com",  "phone": "9000000002", "password": "Doctor@123",  "role": UserRole.DOCTOR},
    {"full_name": "Dr. Priya Nair","email": "doctor2@pranavibhuti.com",  "phone": "9000000003", "password": "Doctor@123",  "role": UserRole.DOCTOR},
    {"full_name": "Arjun Reddy",   "email": "patient1@pranavibhuti.com", "phone": "9000000004", "password": "Patient@123", "role": UserRole.PATIENT},
    {"full_name": "Sneha Sharma",  "email": "patient2@pranavibhuti.com", "phone": "9000000005", "password": "Patient@123", "role": UserRole.PATIENT},
]

SAMPLE_DOCTORS = [
    {
        "email": "doctor1@pranavibhuti.com",
        "profile": {
            "name": "Dr. Ravi Kumar",
            "email": "doctor1@pranavibhuti.com",
            "phone": "9000000002",
            "specialization": "Cardiologist",
            "qualification": "MBBS, MD (Cardiology)",
            "hospital_name": "PRANAVIBHUTI Heart Centre",
            "experience_years": 12,
            "consultation_fee": 800.00,
            "bio": "Experienced cardiologist specializing in heart disease prevention.",
            "is_verified": True,
        }
    },
    {
        "email": "doctor2@pranavibhuti.com",
        "profile": {
            "name": "Dr. Priya Nair",
            "email": "doctor2@pranavibhuti.com",
            "phone": "9000000003",
            "specialization": "Dermatologist",
            "qualification": "MBBS, MD (Dermatology)",
            "hospital_name": "PRANAVIBHUTI Skin Clinic",
            "experience_years": 8,
            "consultation_fee": 600.00,
            "bio": "Specialist in skin disorders, cosmetic dermatology.",
            "is_verified": True,
        }
    }
]


async def seed():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        try:
            # Create users
            user_map = {}
            for u in SAMPLE_USERS:
                user = User(
                    full_name=u["full_name"],
                    email=u["email"],
                    phone=u["phone"],
                    hashed_password=hash_password(u["password"]),
                    role=u["role"],
                    is_active=True,
                    is_verified=True,
                )
                db.add(user)
                await db.flush()
                user_map[u["email"]] = user.id
                print(f"  ✅ User: {u['email']} ({u['role'].value})")

            # Create doctor profiles
            doctor_map = {}
            for d in SAMPLE_DOCTORS:
                uid = user_map[d["email"]]
                doctor = Doctor(user_id=uid, **d["profile"])
                db.add(doctor)
                await db.flush()
                doctor_map[d["email"]] = doctor.id
                print(f"  ✅ Doctor profile: {d['profile']['name']}")

            # Create slots for each doctor (next 3 days, 4 slots/day)
            today = date.today()
            slot_times = [
                (time(9, 0), time(9, 30)),
                (time(10, 0), time(10, 30)),
                (time(14, 0), time(14, 30)),
                (time(15, 0), time(15, 30)),
            ]
            for email, doc_id in doctor_map.items():
                for day_offset in range(1, 4):
                    slot_date = today + timedelta(days=day_offset)
                    for start, end in slot_times:
                        slot = DoctorSlot(
                            doctor_id=doc_id,
                            slot_date=slot_date,
                            start_time=start,
                            end_time=end,
                        )
                        db.add(slot)
                print(f"  ✅ Slots created for doctor_id={doc_id}")

            await db.commit()
            print("\n🎉 Seed complete! Login credentials:")
            print("  Admin:    admin@pranavibhuti.com    / Admin@123")
            print("  Doctor 1: doctor1@pranavibhuti.com / Doctor@123")
            print("  Doctor 2: doctor2@pranavibhuti.com / Doctor@123")
            print("  Patient 1:patient1@pranavibhuti.com/ Patient@123")
            print("  Patient 2:patient2@pranavibhuti.com/ Patient@123")

        except Exception as e:
            await db.rollback()
            print(f"❌ Seed failed: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed())
