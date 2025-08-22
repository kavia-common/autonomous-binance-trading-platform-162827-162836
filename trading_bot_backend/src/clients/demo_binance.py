"""
Demo Binance client (paper trading).

Provides minimal price fetch and order placement simulation for demo mode.
"""
from src.domain.enums import OrderSide, OrderType


class DemoBinanceClient:
    """Simple deterministic price generator and order simulator."""

    # PUBLIC_INTERFACE
    def price(self, symbol: str) -> float:
        """Return a pseudo-random deterministic price for a symbol."""
        base = sum(ord(c) for c in symbol) % 500
        return 100.0 + float(base)

    # PUBLIC_INTERFACE
    def place_order(self, symbol: str, side: OrderSide, order_type: OrderType, quantity: float) -> dict:
        """Simulate placing an order and returning execution details."""
        return {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "price": self.price(symbol),
        }
