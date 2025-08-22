"""
Analytics service for AI performance and metrics.
"""
from typing import List
from datetime import datetime, timedelta

from src.domain.models import AnalyticsSnapshot, PerformanceMetric


class AnalyticsService:
    """Service for analytics and performance data retrieval."""

    # PUBLIC_INTERFACE
    def get_snapshot(self, user_id: str) -> AnalyticsSnapshot:
        """Return analytics snapshot for dashboard with demo seed metrics."""
        metrics = self.stream_metrics_seed(user_id)
        return AnalyticsSnapshot(user_id=user_id, metrics=metrics)

    # PUBLIC_INTERFACE
    def stream_metrics_seed(self, user_id: str) -> List[PerformanceMetric]:
        """Return a seed list of metrics for initial dashboard load."""
        now = datetime.utcnow()
        out: List[PerformanceMetric] = []
        equity = 10000.0
        pnl = 0.0
        drawdown = 0.0
        for i in range(10):
            # fabricate slight changes
            equity *= 1 + (0.001 * ((i % 3) - 1))  # small up/down/no change
            pnl = equity - 10000.0
            drawdown = max(drawdown, abs(pnl) / 10000.0)
            out.append(
                PerformanceMetric(
                    timestamp=now - timedelta(minutes=(10 - i) * 5),
                    equity=round(equity, 2),
                    pnl=round(pnl, 2),
                    drawdown=round(drawdown * 100.0, 2),
                )
            )
        return out
