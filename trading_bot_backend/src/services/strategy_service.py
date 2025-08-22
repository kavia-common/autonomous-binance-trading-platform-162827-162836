"""
Strategy configuration service skeleton.
"""
from typing import List
from pydantic import BaseModel, Field

from src.domain.models import StrategyConfig


class UpsertStrategyRequest(BaseModel):
    """Create/update strategy request."""
    name: str = Field(..., description="Strategy name.")
    parameters: dict = Field(default_factory=dict, description="Parameters map.")
    enabled: bool = Field(default=True, description="Enable/disable strategy.")


class StrategyService:
    """Service for managing strategies."""

    # PUBLIC_INTERFACE
    def list_strategies(self, user_id: str) -> List[StrategyConfig]:
        """Return list of strategies."""
        return []

    # PUBLIC_INTERFACE
    def upsert_strategy(self, user_id: str, data: UpsertStrategyRequest) -> StrategyConfig:
        """Create or update a strategy."""
        return StrategyConfig(id="placeholder", name=data.name, parameters=data.parameters, enabled=data.enabled)
