# app/core/config.py
"""
Central configuration — reads from .env file.
Every team member imports settings from here.

Usage:
    from app.core.config import settings
    print(settings.DATABASE_URL)
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):

    # ── App ───────────────────────────────────────────────────────────────────
    APP_NAME: str = "PRANAVIBHUTI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_URL: str

    # ── JWT ───────────────────────────────────────────────────────────────────
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── File Uploads ──────────────────────────────────────────────────────────
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10

    # ── Notifications (Phase 3) ───────────────────────────────────────────────
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""

    # ── Payment (Phase 3) ─────────────────────────────────────────────────────
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""

    # ── AWS S3 — Health Locker (Phase 3) ──────────────────────────────────────
    AWS_ACCESS_KEY: str = ""
    AWS_SECRET_KEY: str = ""
    AWS_BUCKET_NAME: str = ""
    AWS_REGION: str = "ap-south-1"

    @property
    def origins_list(self) -> List[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
