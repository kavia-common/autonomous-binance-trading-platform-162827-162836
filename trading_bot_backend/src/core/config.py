"""
Application configuration management using environment variables.

This module defines configuration data models used across the backend application.
It provides a single get_settings() entrypoint to retrieve settings.
"""
import os
from functools import lru_cache
from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    """Global application settings loaded from environment."""

    app_name: str = Field(default_factory=lambda: os.getenv("APP_NAME", "Autonomous Binance Trading Backend"), description="Application display name.")
    environment: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"), description="Application environment identifier.")
    debug: bool = Field(default_factory=lambda: os.getenv("DEBUG", "true").lower() == "true", description="Enable/disable debug mode.")
    cors_allow_origins: list[str] = Field(default_factory=lambda: os.getenv("CORS_ALLOW_ORIGINS", "*").split(","), description="CORS allowed origins.")

    # Security
    jwt_secret_key: str = Field(default_factory=lambda: os.getenv("JWT_SECRET_KEY", "CHANGE_ME"), description="JWT secret key (use env in production).")
    jwt_algorithm: str = Field(default_factory=lambda: os.getenv("JWT_ALGORITHM", "HS256"), description="JWT signing algorithm.")
    access_token_expire_minutes: int = Field(default_factory=lambda: int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")), description="Access token validity in minutes.")

    # Binance/API
    binance_api_key: str = Field(default_factory=lambda: os.getenv("BINANCE_API_KEY", ""), description="Binance API Key.")
    binance_api_secret: str = Field(default_factory=lambda: os.getenv("BINANCE_API_SECRET", ""), description="Binance API Secret.")

    # Database connection
    # Example: sqlite:///./app.db  OR  postgresql+psycopg://user:pass@host:5432/db
    database_url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", ""), description="Database connection URL (e.g., SQLite/PG).")

    # WebSocket
    ws_allowed_origins: list[str] = Field(default_factory=lambda: os.getenv("WS_ALLOWED_ORIGINS", "*").split(","), description="Allowed WS origins.")


# PUBLIC_INTERFACE
@lru_cache()
def get_settings() -> AppSettings:
    """Return cached application settings loaded from environment."""
    return AppSettings()
