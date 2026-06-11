# app/core/exceptions.py
"""
Global exception handlers — registered in main.py.
Every team member benefits from these automatically.
No need to handle 404/422/500 manually in your routes.
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

try:
    from sqlalchemy.exc import IntegrityError
except ImportError:
    class IntegrityError(Exception):
        pass


def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"success": False, "message": "Resource not found.", "data": None},
    )


def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"] if loc != "body")
        errors.append({"field": field, "message": err["msg"]})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "message": "Validation failed.", "errors": errors},
    )


def integrity_error_handler(request: Request, exc: IntegrityError):
    detail = str(getattr(exc, "orig", exc))
    if "unique" in detail.lower() or "duplicate" in detail.lower():
        message = "A record with this data already exists."
    elif "foreign key" in detail.lower():
        message = "Referenced record does not exist."
    else:
        message = "Database constraint violation."
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"success": False, "message": message, "data": None},
    )


def internal_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": "Internal server error. Please try again.", "data": None},
    )
