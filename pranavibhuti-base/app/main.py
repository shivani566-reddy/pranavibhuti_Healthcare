# app/main.py
"""
PRANAVIBHUTI — Main Application Entry Point

Run with:
    uvicorn app.main:app --reload

Swagger docs:
    http://localhost:8000/docs

ReDoc:
    http://localhost:8000/redoc
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.exceptions import (
    validation_error_handler,
    integrity_error_handler,
    internal_error_handler,
)
from app.db.session import engine
from app.db.base import Base
from app.api.v1.router import api_router

# Import ALL models so SQLAlchemy registers them before create_all
import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs on startup and shutdown."""
    # Create all tables automatically on first run
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created / verified.")
    yield
    await engine.dispose()
    print("✅ Database connections closed.")


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Complete healthcare ecosystem — Authentication, Doctors, Appointments, "
        "Pharmacy, Lab, Health Locker, Telemedicine, AI Assistant, Payments."
    ),
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global exception handlers ─────────────────────────────────────────────────
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, internal_error_handler)

# ── All API routes ─────────────────────────────────────────────────────────────
app.include_router(api_router)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}
