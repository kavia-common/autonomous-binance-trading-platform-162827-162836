import os
import pytest
from datetime import timedelta
from fastapi.testclient import TestClient

# Ensure test uses a temp SQLite DB file under project root
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_app.db")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "5")
os.environ.setdefault("CORS_ALLOW_ORIGINS", "*")

from src.api.main import app  # noqa: E402
from src.infrastructure.db import init_db, db_session, UserORM  # noqa: E402
from src.core.security import get_password_hash, create_access_token  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Initialize DB schema and ensure a clean start.
    """
    # Initialize tables
    init_db()
    # Cleanup any prior users with our test email to avoid uniqueness issues
    with db_session() as db:
        db.query(UserORM).delete()
    yield
    # Teardown: remove test db file if using file-based sqlite
    db_url = os.getenv("DATABASE_URL", "")
    if db_url.startswith("sqlite:///./"):
        db_path = db_url.replace("sqlite:///", "")
        try:
            if os.path.exists(db_path):
                os.remove(db_path)
        except Exception:
            # ignore cleanup errors
            pass


@pytest.fixture(scope="session")
def client():
    """
    Provide a FastAPI TestClient bound to our app.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def seed_user():
    """
    Seed a real user in DB to satisfy get_current_user(), since /auth/login returns a placeholder token.
    Returns dict with user_id and email.
    """
    email = "testuser@example.com"
    password = "TestPass123!"
    password_hash = get_password_hash(password)
    user_id = "user-1"
    with db_session() as db:
        # Seed concrete user the security layer will load from DB
        user = UserORM(
            id=user_id,
            email=email,
            full_name="Test User",
            password_hash=password_hash,
            is_active=True,
        )
        db.add(user)
        db.flush()
    return {"user_id": user_id, "email": email, "password": password}


@pytest.fixture
def bearer_token(seed_user):
    """
    Create a valid JWT access token for the seeded user.
    Note: The /auth/login endpoint currently returns a placeholder token that does not pass get_current_user validation.
    We therefore create a valid token directly for protected endpoints.
    """
    token = create_access_token(subject=seed_user["user_id"], expires_delta=timedelta(minutes=5))
    return token


@pytest.fixture
def auth_header(bearer_token):
    """
    Standard Authorization header for authenticated calls.
    """
    return {"Authorization": f"Bearer {bearer_token}"}
