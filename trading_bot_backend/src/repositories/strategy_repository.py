"""
Strategy repository backed by SQLAlchemy.
"""
from typing import Optional, List
from uuid import uuid4

from sqlalchemy import select, delete, update

from src.domain.models import StrategyConfig
from src.infrastructure.db import db_session, StrategyORM
from src.repositories.base import Repository


def _to_domain(s: StrategyORM) -> StrategyConfig:
    return StrategyConfig(
        id=s.id,
        name=s.name,
        parameters={k: float(v) if isinstance(v, (int, float)) else v for k, v in (s.parameters or {}).items()},
        enabled=s.enabled,
    )


class StrategyRepository(Repository[StrategyConfig]):
    """Strategy repository implementing base methods via SQLAlchemy."""

    # PUBLIC_INTERFACE
    def get(self, item_id: str) -> Optional[StrategyConfig]:
        """Fetch a strategy by ID."""
        with db_session() as db:
            orm = db.get(StrategyORM, item_id)
            return _to_domain(orm) if orm else None

    # PUBLIC_INTERFACE
    def list_by_user(self, user_id: str) -> List[StrategyConfig]:
        """List all strategies for a user."""
        with db_session() as db:
            res = db.execute(select(StrategyORM).where(StrategyORM.user_id == user_id)).scalars().all()
            return [_to_domain(s) for s in res]

    # PUBLIC_INTERFACE
    def list(self) -> List[StrategyConfig]:
        """List all strategies."""
        with db_session() as db:
            res = db.execute(select(StrategyORM)).scalars().all()
            return [_to_domain(s) for s in res]

    # PUBLIC_INTERFACE
    def upsert_for_user(self, user_id: str, item: StrategyConfig) -> StrategyConfig:
        """Create or update a strategy for a user by name."""
        with db_session() as db:
            existing = db.execute(
                select(StrategyORM).where(StrategyORM.user_id == user_id, StrategyORM.name == item.name)
            ).scalar_one_or_none()
            if existing:
                db.execute(
                    update(StrategyORM)
                    .where(StrategyORM.id == existing.id)
                    .values(parameters=item.parameters, enabled=item.enabled)
                )
                orm = db.get(StrategyORM, existing.id)
            else:
                orm = StrategyORM(
                    id=item.id or str(uuid4()),
                    user_id=user_id,
                    name=item.name,
                    parameters=item.parameters,
                    enabled=item.enabled,
                )
                db.add(orm)
                db.flush()
            return _to_domain(orm)

    # PUBLIC_INTERFACE
    def create(self, item: StrategyConfig) -> StrategyConfig:
        """Create a strategy (system-wide; prefer upsert_for_user)."""
        with db_session() as db:
            orm = StrategyORM(
                id=item.id or str(uuid4()),
                user_id="system",
                name=item.name,
                parameters=item.parameters,
                enabled=item.enabled,
            )
            db.add(orm)
            db.flush()
            return _to_domain(orm)

    # PUBLIC_INTERFACE
    def update(self, item_id: str, item: StrategyConfig) -> StrategyConfig:
        """Update a strategy."""
        with db_session() as db:
            db.execute(
                update(StrategyORM)
                .where(StrategyORM.id == item_id)
                .values(name=item.name, parameters=item.parameters, enabled=item.enabled)
            )
            orm = db.get(StrategyORM, item_id)
            return _to_domain(orm)

    # PUBLIC_INTERFACE
    def delete(self, item_id: str) -> None:
        """Delete a strategy."""
        with db_session() as db:
            db.execute(delete(StrategyORM).where(StrategyORM.id == item_id))
            return None
