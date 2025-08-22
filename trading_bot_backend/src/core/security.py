"""
Security utilities and interfaces.

Contains helpers for password hashing, token creation/validation, and FastAPI dependencies.
"""
from typing import Optional
from datetime import timedelta, datetime, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.core.config import get_settings
from src.infrastructure.db import db_session, UserORM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    """Access token response model."""
    access_token: str = Field(..., description="JWT access token string.")
    token_type: str = Field(default="bearer", description="Token type; typically 'bearer'.")


class TokenPayload(BaseModel):
    """Decoded JWT payload structure."""
    sub: str = Field(..., description="Subject (typically user ID).")
    exp: int = Field(..., description="Expiration timestamp.")


# PUBLIC_INTERFACE
def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create and return a signed JWT for the given subject."""
    settings = get_settings()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


# PUBLIC_INTERFACE
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


# PUBLIC_INTERFACE
def get_password_hash(password: str) -> str:
    """Return a hashed version of the password."""
    return pwd_context.hash(password)


# PUBLIC_INTERFACE
def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    FastAPI dependency that validates the bearer token and returns current user context.

    Returns:
        dict: {"user_id": "<id>", "email": "<email>"}
    """
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    with db_session() as db:
        user = db.get(UserORM, sub)
        if user is None or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")

        return {"user_id": user.id, "email": user.email}
