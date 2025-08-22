"""
Authentication routes skeleton.
"""
from fastapi import APIRouter, Depends
from src.services.auth_service import AuthService, LoginRequest, SignupRequest
from src.core.security import Token, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])
_service = AuthService()


@router.post("/login", response_model=Token, summary="Login", description="Authenticate and receive an access token.")
# PUBLIC_INTERFACE
def login(data: LoginRequest) -> Token:
    """Authenticate a user and return an access token."""
    return _service.login(data)


@router.post("/signup", summary="Signup", description="Create a new user account.")
# PUBLIC_INTERFACE
def signup(data: SignupRequest) -> dict:
    """Create a user and return basic user info."""
    user = _service.signup(data)
    return user.model_dump()


@router.get("/me", summary="Me", description="Return current user profile.")
# PUBLIC_INTERFACE
def me(user=Depends(get_current_user)) -> dict:
    """Return the current user's profile."""
    profile = _service.me(user_id=user["user_id"])
    return profile.model_dump()
