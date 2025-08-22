"""
Analytics service skeleton for AI performance and metrics.
"""
from typing import List
from src.domain.models import AnalyticsSnapshot, PerformanceMetric


class AnalyticsService:
    """Service for analytics and performance data retrieval."""

    # PUBLIC_INTERFACE
    def get_snapshot(self, user_id: str) -> AnalyticsSnapshot:
        """Return analytics snapshot for dashboard."""
        return AnalyticsSnapshot(user_id=user_id, metrics=[])

    # PUBLIC_INTERFACE
    def stream_metrics_seed(self, user_id: str) -> List[PerformanceMetric]:
        """Return a seed list of metrics for initial dashboard load."""
        return []
