"""
Trade repository backed by SQLAlchemy.
"""
from typing import Optional, List
from uuid import uuid4

from sqlalchemy import select, delete, update

from src.domain.models import Trade
from src.infrastructure.db import db_session, TradeORM
from src.repositories.base import Repository


def _to_domain(t: TradeORM) -> Trade:
    return Trade(
        id=t.id,
        user_id=t.user_id,
        symbol=t.symbol,
        side=t.side,
        type=t.type,
        quantity=t.quantity,
        price=t.price,
        mode=t.mode,
        created_at=t.created_at,
    )


class TradeRepository(Repository[Trade]):
    """Trade repository implementing base methods via SQLAlchemy."""

    # PUBLIC_INTERFACE
    def get(self, item_id: str) -> Optional[Trade]:
        """Fetch a trade by ID."""
        with db_session() as db:
            orm = db.get(TradeORM, item_id)
            return _to_domain(orm) if orm else None

    # PUBLIC_INTERFACE
    def list(self) -> List[Trade]:
        """List all trades."""
        with db_session() as db:
            res = db.execute(select(TradeORM)).scalars().all()
            return [_to_domain(t) for t in res]

    # PUBLIC_INTERFACE
    def list_by_user(self, user_id: str) -> List[Trade]:
        """List all trades for a user."""
        with db_session() as db:
            res = db.execute(select(TradeORM).where(TradeORM.user_id == user_id).order_by(TradeORM.created_at.desc())).scalars().all()
            return [_to_domain(t) for t in res]

    # PUBLIC_INTERFACE
    def create(self, item: Trade) -> Trade:
        """Create a trade."""
        with db_session() as db:
            orm = TradeORM(
                id=item.id or str(uuid4()),
                user_id=item.user_id,
                symbol=item.symbol,
                side=item.side,
                type=item.type,
                quantity=item.quantity,
                price=item.price,
                mode=item.mode,
                created_at=item.created_at,
            )
            db.add(orm)
            db.flush()
            return _to_domain(orm)

    # PUBLIC_INTERFACE
    def update(self, item_id: str, item: Trade) -> Trade:
        """Update a trade."""
        with db_session() as db:
            db.execute(
                update(TradeORM)
                .where(TradeORM.id == item_id)
                .values(
                    symbol=item.symbol,
                    side=item.side,
                    type=item.type,
                    quantity=item.quantity,
                    price=item.price,
                    mode=item.mode,
                )
            )
            orm = db.get(TradeORM, item_id)
            return _to_domain(orm)

    # PUBLIC_INTERFACE
    def delete(self, item_id: str) -> None:
        """Delete a trade."""
        with db_session() as db:
            db.execute(delete(TradeORM).where(TradeORM.id == item_id))
            return None
