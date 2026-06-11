# app/core/response.py
"""
Standard response format — ALL team members must use this.
Every API response will have the same shape so the frontend
(Akhil Reddy) can handle responses consistently.

Response shape:
{
    "success": true,
    "message": "Doctor profile created.",
    "data": { ... }        ← actual data or null
}

Usage:
    from app.core.response import success_response, error_response

    return success_response("Appointment booked.", appointment_data)
    return error_response("Slot not available.", status_code=409)
"""
from fastapi.responses import JSONResponse
from typing import Any, Optional


def success_response(
    message: str,
    data: Any = None,
    status_code: int = 200,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data,
        },
    )


def error_response(
    message: str,
    status_code: int = 400,
    data: Any = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": data,
        },
    )


def paginated_response(
    message: str,
    data: list,
    total: int,
    page: int,
    limit: int,
) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "data": data,
            "pagination": {
                "total": total,
                "page": page,
                "limit": limit,
                "pages": (total + limit - 1) // limit,
            },
        },
    )
