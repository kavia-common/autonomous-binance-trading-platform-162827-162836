"""
Trade repository interface skeleton.
"""
from typing import Optional, List
from src.domain.models import Trade
from src.repositories.base import Repository


class TradeRepository(Repository[Trade]):
    """Trade repository implementing base methods (skeleton)."""

    # PUBLIC_INTERFACE
    def get(self, item_id: str) -> Optional[Trade]:
        """Fetch a trade by ID."""
        return None

    # PUBLIC_INTERFACE
    def list(self) -> List[Trade]:
        """List all trades."""
        return []

    # PUBLIC_INTERFACE
    def create(self, item: Trade) -> Trade:
        """Create a trade."""
        return item

    # PUBLIC_INTERFACE
    def update(self, item_id: str, item: Trade) -> Trade:
        """Update a trade."""
        return item

    # PUBLIC_INTERFACE
    def delete(self, item_id: str) -> None:
        """Delete a trade."""
        return None
