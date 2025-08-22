"""
Trading orchestration service skeleton.
"""
from typing import List
from pydantic import BaseModel, Field

from src.domain.enums import TradingMode, OrderSide, OrderType
from src.domain.models import Trade


class PlaceOrderRequest(BaseModel):
    """Place order request."""
    symbol: str = Field(..., description="Symbol pair, e.g., BTCUSDT.")
    side: OrderSide = Field(..., description="Order side.")
    type: OrderType = Field(..., description="Order type.")
    quantity: float = Field(..., description="Order quantity.")


class SwitchModeRequest(BaseModel):
    """Switch trading mode request."""
    mode: TradingMode = Field(..., description="New trading mode.")


class TradingService:
    """Service for executing trades and handling trading mode."""

    # PUBLIC_INTERFACE
    def place_order(self, user_id: str, data: PlaceOrderRequest) -> Trade:
        """Place an order and return a trade record."""
        return Trade(
            id="placeholder",
            user_id=user_id,
            symbol=data.symbol,
            side=data.side,
            type=data.type,
            quantity=data.quantity,
            price=None,
        )

    # PUBLIC_INTERFACE
    def get_trades(self, user_id: str) -> List[Trade]:
        """List trades for the user."""
        return []

    # PUBLIC_INTERFACE
    def switch_mode(self, user_id: str, data: SwitchModeRequest) -> TradingMode:
        """Switch user trading mode."""
        return data.mode
