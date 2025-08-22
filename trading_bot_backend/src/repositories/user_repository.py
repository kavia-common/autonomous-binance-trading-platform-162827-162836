"""
User repository backed by SQLAlchemy.
"""
from typing import Optional, List
from uuid import uuid4

from sqlalchemy import select, delete, update

from src.domain.models import User
from src.infrastructure.db import db_session, UserORM
from src.repositories.base import Repository


def _to_domain(u: UserORM) -> User:
    return User(
        id=u.id,
        email=u.email,
        full_name=u.full_name,
        is_active=u.is_active,
        created_at=u.created_at,
    )


class UserRepository(Repository[User]):
    """User repository implementing base methods via SQLAlchemy."""

    # PUBLIC_INTERFACE
    def get(self, item_id: str) -> Optional[User]:
        """Fetch a user by ID."""
        with db_session() as db:
            orm = db.get(UserORM, item_id)
            return _to_domain(orm) if orm else None

    # PUBLIC_INTERFACE
    def get_by_email(self, email: str) -> Optional[UserORM]:
        """Return ORM User by email (internal use)."""
        with db_session() as db:
            stmt = select(UserORM).where(UserORM.email == email)
            res = db.execute(stmt).scalar_one_or_none()
            return res

    # PUBLIC_INTERFACE
    def list(self) -> List[User]:
        """List all users."""
        with db_session() as db:
            res = db.execute(select(UserORM)).scalars().all()
            return [_to_domain(u) for u in res]

    # PUBLIC_INTERFACE
    def create(self, item: User, password_hash: str | None = None) -> User:
        """Create a user."""
        with db_session() as db:
            orm = UserORM(
                id=item.id or str(uuid4()),
                email=item.email,
                full_name=item.full_name,
                password_hash=password_hash or "",
                is_active=item.is_active,
                created_at=item.created_at,
            )
            db.add(orm)
            db.flush()
            return _to_domain(orm)

    # PUBLIC_INTERFACE
    def update(self, item_id: str, item: User) -> User:
        """Update a user."""
        with db_session() as db:
            db.execute(
                update(UserORM)
                .where(UserORM.id == item_id)
                .values(email=item.email, full_name=item.full_name, is_active=item.is_active)
            )
            orm = db.get(UserORM, item_id)
            return _to_domain(orm)

    # PUBLIC_INTERFACE
    def delete(self, item_id: str) -> None:
        """Delete a user."""
        with db_session() as db:
            db.execute(delete(UserORM).where(UserORM.id == item_id))
            return None
