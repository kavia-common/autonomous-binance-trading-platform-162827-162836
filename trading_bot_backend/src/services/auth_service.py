"""
Authentication and user-related service skeleton.
"""
from typing import Optional
from pydantic import BaseModel, Field

from src.core.security import Token
from src.domain.models import User


class LoginRequest(BaseModel):
    """Login request model."""
    email: str = Field(..., description="User email.")
    password: str = Field(..., description="User password.")


class SignupRequest(BaseModel):
    """Signup request model."""
    email: str = Field(..., description="User email.")
    password: str = Field(..., description="User password.")
    full_name: Optional[str] = Field(default=None, description="Full name.")


class AuthService:
    """Authentication service interface."""

    # PUBLIC_INTERFACE
    def login(self, data: LoginRequest) -> Token:
        """Authenticate a user and return an access token."""
        return Token(access_token="placeholder", token_type="bearer")

    # PUBLIC_INTERFACE
    def signup(self, data: SignupRequest) -> User:
        """Create a new user account."""
        return User(id="placeholder", email=data.email, full_name=data.full_name, is_active=True)

    # PUBLIC_INTERFACE
    def me(self, user_id: str) -> User:
        """Return profile information for the current user."""
        return User(id=user_id, email="placeholder@example.com", is_active=True)
