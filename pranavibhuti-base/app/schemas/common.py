# app/schemas/common.py
"""
Shared Pydantic schemas — base classes for all team members.

Every team member creates their own schema file, e.g.:
    app/schemas/doctor.py
    app/schemas/pharmacy.py

But they can inherit from or use these base types.
"""
from pydantic import BaseModel
from typing import Any, List, Optional, Generic, TypeVar
from datetime import datetime

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard response wrapper — matches app/core/response.py shape."""
    success: bool
    message: str
    data: Optional[T] = None


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: List[T]
    pagination: dict


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str
    user_id: int


class MessageOnly(BaseModel):
    message: str
