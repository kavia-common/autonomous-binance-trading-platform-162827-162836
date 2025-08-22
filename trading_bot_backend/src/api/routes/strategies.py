"""
Strategy routes skeleton.
"""
from typing import List
from fastapi import APIRouter, Depends

from src.core.security import get_current_user
from src.domain.models import StrategyConfig
from src.services.strategy_service import StrategyService, UpsertStrategyRequest

router = APIRouter(prefix="/strategies", tags=["Strategies"])
_service = StrategyService()


@router.get("/", response_model=list[StrategyConfig], summary="List Strategies", description="List all strategies.")
# PUBLIC_INTERFACE
def list_strategies(user=Depends(get_current_user)) -> List[StrategyConfig]:
    """Return list of strategies for the current user."""
    return _service.list_strategies(user_id=user["user_id"])


@router.post("/", response_model=StrategyConfig, summary="Upsert Strategy", description="Create or update a strategy.")
# PUBLIC_INTERFACE
def upsert_strategy(data: UpsertStrategyRequest, user=Depends(get_current_user)) -> StrategyConfig:
    """Create or update a strategy for the current user."""
    return _service.upsert_strategy(user_id=user["user_id"], data=data)
