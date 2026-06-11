# app/core/dependencies.py
"""
Shared FastAPI dependencies — import and use these in every route.

These are the RBAC gates. Each team member uses the appropriate one
on their routes. Adding the dependency to a route IS the security.

Usage in a route:
    from app.core.dependencies import require_patient

    @router.get("/my-data")
    async def get_data(current_user: dict = Depends(require_patient)):
        patient_id = int(current_user["sub"])
        ...

RBAC Ownership checks (call inside your controller):
    from app.core.dependencies import assert_owner

    assert_owner(resource_owner_id, current_user, "appointment")
    # Raises 403 if the logged-in user doesn't own the resource
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.core.security import verify_token
from app.db.session import get_db

bearer_scheme = HTTPBearer(auto_error=False)


def _extract_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Provide a Bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


def get_current_user(token: str = Depends(_extract_token)) -> dict:
    """
    Base dependency — verifies JWT and returns its payload.
    Any logged-in user (patient, doctor, admin) passes this gate.
    """
    try:
        payload = verify_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token. Please login again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Provide an access token, not a refresh token.",
        )
    return payload


def require_patient(current_user: dict = Depends(get_current_user)) -> dict:
    """Only patients pass this gate. Use on patient-specific routes."""
    if current_user.get("role") != "patient":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient account required.",
        )
    return current_user


def require_doctor(current_user: dict = Depends(get_current_user)) -> dict:
    """Only doctors pass this gate. Use on doctor-specific routes."""
    if current_user.get("role") != "doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Doctor account required.",
        )
    return current_user


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Only admins pass this gate. Use on admin-only routes."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account required.",
        )
    return current_user


def require_doctor_or_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Doctors and admins pass. Use on routes that either role can access."""
    if current_user.get("role") not in ("doctor", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Doctor or Admin account required.",
        )
    return current_user


# ── Row-level ownership checks ────────────────────────────────────────────────

def assert_owner(resource_user_id: int, current_user: dict, resource_name: str = "resource"):
    """
    Verify the logged-in user owns the resource.
    Admins bypass this check — they can access everything.

    Args:
        resource_user_id: the user_id stored on the DB row
        current_user:     decoded JWT payload
        resource_name:    shown in the 403 error message

    Example:
        # Inside appointment controller:
        assert_owner(appointment.patient_id, current_user, "appointment")
    """
    if current_user.get("role") == "admin":
        return   # admins bypass ownership checks
    if int(current_user["sub"]) != resource_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You do not have permission to access this {resource_name}.",
        )
