# tests/test_auth.py
"""
Sample tests — run with:  pytest tests/
Each team member should write tests for their own endpoints.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Register
        reg = await client.post("/api/v1/auth/register", json={
            "full_name": "Test Patient",
            "email": "testpatient@example.com",
            "phone": "9999999999",
            "password": "Test@1234",
            "role": "patient"
        })
        assert reg.status_code == 201
        otp = reg.json()["data"]["otp_for_testing"]

        # Verify OTP
        verify = await client.post("/api/v1/auth/verify-otp", json={
            "email": "testpatient@example.com",
            "otp_code": otp,
        })
        assert verify.status_code == 200

        # Login
        login = await client.post("/api/v1/auth/login", json={
            "email": "testpatient@example.com",
            "password": "Test@1234",
        })
        assert login.status_code == 200
        assert "access_token" in login.json()["data"]


@pytest.mark.asyncio
async def test_list_doctors_public():
    """Public endpoint — no auth needed."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/doctors")
    assert response.status_code == 200
    assert response.json()["success"] is True
