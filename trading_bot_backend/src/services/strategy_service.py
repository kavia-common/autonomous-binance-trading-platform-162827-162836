"""
Strategy configuration service.
"""
from typing import List
from uuid import uuid4
from pydantic import BaseModel, Field

from src.domain.models import StrategyConfig
from src.repositories.strategy_repository import StrategyRepository


class UpsertStrategyRequest(BaseModel):
    """Create/update strategy request."""
    name: str = Field(..., description="Strategy name.")
    parameters: dict = Field(default_factory=dict, description="Parameters map.")
    enabled: bool = Field(default=True, description="Enable/disable strategy.")


class StrategyService:
    """Service for managing strategies."""

    def __init__(self) -> None:
        self._repo = StrategyRepository()

    # PUBLIC_INTERFACE
    def list_strategies(self, user_id: str) -> List[StrategyConfig]:
        """Return list of strategies. Seed with a default if empty."""
        strategies = self._repo.list_by_user(user_id)
        if not strategies:
            # seed a basic demo strategy
            demo = StrategyConfig(
                id=str(uuid4()),
                name="Demo Mean Reversion",
                parameters={"lookback": 14, "threshold": 1.5},
                enabled=True,
            )
            self._repo.upsert_for_user(user_id, demo)
            strategies = self._repo.list_by_user(user_id)
        return strategies

    # PUBLIC_INTERFACE
    def upsert_strategy(self, user_id: str, data: UpsertStrategyRequest) -> StrategyConfig:
        """Create or update a strategy."""
        cfg = StrategyConfig(id=str(uuid4()), name=data.name, parameters=data.parameters, enabled=data.enabled)
        return self._repo.upsert_for_user(user_id, cfg)
