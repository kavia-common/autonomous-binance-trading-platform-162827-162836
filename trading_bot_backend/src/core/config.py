"""
Application configuration management using environment variables.

This module defines configuration data models used across the backend application.
It provides a single get_settings() entrypoint to retrieve settings.
"""
from functools import lru_cache
from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    """Global application settings loaded from environment."""

    app_name: str = Field(default="Autonomous Binance Trading Backend", description="Application display name.")
    environment: str = Field(default="development", description="Application environment identifier.")
    debug: bool = Field(default=True, description="Enable/disable debug mode.")
    cors_allow_origins: list[str] = Field(default_factory=lambda: ["*"], description="CORS allowed origins.")

    # Security
    jwt_secret_key: str = Field(default="CHANGE_ME", description="JWT secret key (use env in production).")
    jwt_algorithm: str = Field(default="HS256", description="JWT signing algorithm.")
    access_token_expire_minutes: int = Field(default=60, description="Access token validity in minutes.")

    # Binance/API
    binance_api_key: str = Field(default="", description="Binance API Key.")
    binance_api_secret: str = Field(default="", description="Binance API Secret.")

    # Database connection (to be provided by database container via .env)
    database_url: str = Field(default="", description="Database connection URL (e.g., PostgreSQL/SQLite).")

    # WebSocket
    ws_allowed_origins: list[str] = Field(default_factory=lambda: ["*"], description="Allowed WS origins.")


# PUBLIC_INTERFACE
@lru_cache()
def get_settings() -> AppSettings:
    """Return cached application settings loaded from environment."""
    # Note: In future we can load from environment automatically with pydantic-settings.
    return AppSettings()
