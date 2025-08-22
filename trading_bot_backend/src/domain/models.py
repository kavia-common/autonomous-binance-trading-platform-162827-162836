"""
Domain models for the trading bot backend.

Contains pydantic BaseModel schemas for user, strategy configurations,
trades, performance analytics, and notifications.
"""
from datetime import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel, Field

from src.domain.enums import TradingMode, OrderSide, OrderType


class User(BaseModel):
    """User account model."""
    id: str = Field(..., description="Unique user identifier.")
    email: str = Field(..., description="Email address.")
    full_name: Optional[str] = Field(default=None, description="Full name.")
    is_active: bool = Field(default=True, description="Active flag.")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp.")


class StrategyConfig(BaseModel):
    """Strategy configuration model."""
    id: str = Field(..., description="Strategy identifier.")
    name: str = Field(..., description="Strategy name.")
    parameters: Dict[str, float] = Field(default_factory=dict, description="Numeric parameters map.")
    enabled: bool = Field(default=True, description="Whether the strategy is active.")


class Trade(BaseModel):
    """Trade record model."""
    id: str = Field(..., description="Trade ID.")
    user_id: str = Field(..., description="Owner user ID.")
    symbol: str = Field(..., description="Symbol pair, e.g., BTCUSDT.")
    side: OrderSide = Field(..., description="Order side.")
    type: OrderType = Field(..., description="Order type.")
    quantity: float = Field(..., description="Quantity traded.")
    price: Optional[float] = Field(default=None, description="Executed price for LIMIT or filled price.")
    mode: TradingMode = Field(default=TradingMode.DEMO, description="Trading mode.")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp.")


class PerformanceMetric(BaseModel):
    """Performance analytics data point."""
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Data timestamp.")
    equity: float = Field(..., description="Account equity value.")
    pnl: float = Field(..., description="Profit and loss.")
    drawdown: float = Field(..., description="Drawdown percent.")


class AnalyticsSnapshot(BaseModel):
    """Snapshot of analytics metrics for a dashboard."""
    user_id: str = Field(..., description="Owner user ID.")
    metrics: List[PerformanceMetric] = Field(default_factory=list, description="Series of metrics.")
