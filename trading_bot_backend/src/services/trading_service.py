"""
Trading orchestration service with demo client and persistence.
"""
from typing import List
from uuid import uuid4
from pydantic import BaseModel, Field

from src.domain.enums import TradingMode, OrderSide, OrderType
from src.domain.models import Trade
from src.repositories.trade_repository import TradeRepository
from src.infrastructure.db import db_session, UserSettingORM
from src.clients.demo_binance import DemoBinanceClient


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

    def __init__(self) -> None:
        self._repo = TradeRepository()
        self._demo = DemoBinanceClient()

    def _get_user_mode(self, user_id: str) -> TradingMode:
        with db_session() as db:
            setting = db.query(UserSettingORM).filter(
                UserSettingORM.user_id == user_id, UserSettingORM.key == "trading_mode"
            ).first()
            if setting and setting.value in (TradingMode.DEMO.value, TradingMode.LIVE.value):
                return TradingMode(setting.value)
            return TradingMode.DEMO

    # PUBLIC_INTERFACE
    def place_order(self, user_id: str, data: PlaceOrderRequest) -> Trade:
        """Place an order and return a trade record."""
        mode = self._get_user_mode(user_id)
        # For MVP/demo, always execute via demo client
        exec_info = self._demo.place_order(data.symbol, data.side, data.type, data.quantity)
        trade = Trade(
            id=str(uuid4()),
            user_id=user_id,
            symbol=exec_info["symbol"],
            side=exec_info["side"],
            type=exec_info["type"],
            quantity=exec_info["quantity"],
            price=exec_info["price"],
            mode=mode,
        )
        return self._repo.create(trade)

    # PUBLIC_INTERFACE
    def get_trades(self, user_id: str) -> List[Trade]:
        """List trades for the user."""
        return self._repo.list_by_user(user_id)

    # PUBLIC_INTERFACE
    def switch_mode(self, user_id: str, data: SwitchModeRequest) -> TradingMode:
        """Switch user trading mode (persist setting)."""
        with db_session() as db:
            setting = db.query(UserSettingORM).filter(
                UserSettingORM.user_id == user_id, UserSettingORM.key == "trading_mode"
            ).first()
            if setting:
                setting.value = data.mode.value
            else:
                db.add(UserSettingORM(user_id=user_id, key="trading_mode", value=data.mode.value))
        return data.mode
