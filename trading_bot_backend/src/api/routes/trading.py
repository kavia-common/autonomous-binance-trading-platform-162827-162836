"""
Trading routes skeleton.
"""
from typing import List
from fastapi import APIRouter, Depends

from src.core.security import get_current_user
from src.domain.enums import TradingMode
from src.domain.models import Trade
from src.services.trading_service import TradingService, PlaceOrderRequest, SwitchModeRequest

router = APIRouter(prefix="/trading", tags=["Trading"])
_service = TradingService()


@router.post("/order", response_model=Trade, summary="Place Order", description="Place a trading order.")
# PUBLIC_INTERFACE
def place_order(data: PlaceOrderRequest, user=Depends(get_current_user)) -> Trade:
    """Place a trading order for the current user."""
    return _service.place_order(user_id=user["user_id"], data=data)


@router.get("/trades", response_model=list[Trade], summary="List Trades", description="List user trades.")
# PUBLIC_INTERFACE
def list_trades(user=Depends(get_current_user)) -> List[Trade]:
    """Return a list of user's trades."""
    return _service.get_trades(user_id=user["user_id"])


@router.post("/mode", response_model=TradingMode, summary="Switch Mode", description="Switch trading mode (Demo/Live).")
# PUBLIC_INTERFACE
def switch_mode(data: SwitchModeRequest, user=Depends(get_current_user)) -> TradingMode:
    """Switch trading mode for the current user."""
    return _service.switch_mode(user_id=user["user_id"], data=data)
