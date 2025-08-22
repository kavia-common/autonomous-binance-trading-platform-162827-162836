"""
Strategy repository interface skeleton.
"""
from typing import Optional, List
from src.domain.models import StrategyConfig
from src.repositories.base import Repository


class StrategyRepository(Repository[StrategyConfig]):
    """Strategy repository implementing base methods (skeleton)."""

    # PUBLIC_INTERFACE
    def get(self, item_id: str) -> Optional[StrategyConfig]:
        """Fetch a strategy by ID."""
        return None

    # PUBLIC_INTERFACE
    def list(self) -> List[StrategyConfig]:
        """List all strategies."""
        return []

    # PUBLIC_INTERFACE
    def create(self, item: StrategyConfig) -> StrategyConfig:
        """Create a strategy."""
        return item

    # PUBLIC_INTERFACE
    def update(self, item_id: str, item: StrategyConfig) -> StrategyConfig:
        """Update a strategy."""
        return item

    # PUBLIC_INTERFACE
    def delete(self, item_id: str) -> None:
        """Delete a strategy."""
        return None
