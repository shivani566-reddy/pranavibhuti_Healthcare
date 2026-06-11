# app/db/base.py
"""
SQLAlchemy Base — ALL models must inherit from this Base.

Usage:
    from app.db.base import Base

    class Doctor(Base):
        __tablename__ = "doctors"
        id = Column(Integer, primary_key=True)
        ...

The BaseModel mixin adds created_at and updated_at to every table
that needs it. Inherit from both:

    class Doctor(TimestampMixin, Base):
        ...
"""
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime
from datetime import datetime


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    """Adds created_at and updated_at columns to any model."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
