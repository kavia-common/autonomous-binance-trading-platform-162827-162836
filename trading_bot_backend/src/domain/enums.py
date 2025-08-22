"""
Domain enums for trading modes, order sides/types, and notification channels.
"""
from enum import Enum


class TradingMode(str, Enum):
    """Trading mode indicator."""
    DEMO = "DEMO"
    LIVE = "LIVE"


class OrderSide(str, Enum):
    """Order side."""
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    """Order type."""
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class NotificationChannel(str, Enum):
    """Notification channel type."""
    EMAIL = "EMAIL"
    WEBHOOK = "WEBHOOK"
    IN_APP = "IN_APP"
