"""
Analytics routes and WebSocket help skeleton.
"""
from fastapi import APIRouter

from src.domain.models import AnalyticsSnapshot
from src.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])
_service = AnalyticsService()


@router.get("/snapshot", response_model=AnalyticsSnapshot, summary="Analytics Snapshot", description="Return analytics snapshot for dashboard.")
# PUBLIC_INTERFACE
def analytics_snapshot(user_id: str = "placeholder") -> AnalyticsSnapshot:
    """Return analytics snapshot. Placeholder user_id until auth wiring is finalized."""
    return _service.get_snapshot(user_id=user_id)


@router.get("/websocket-info", summary="WebSocket Usage", description="How to connect to analytics WebSocket and receive updates.", tags=["WebSocket"])
# PUBLIC_INTERFACE
def websocket_usage() -> dict:
    """Return WebSocket usage instructions for clients."""
    return {
        "endpoint": "/ws/analytics",
        "note": "Connect via WebSocket and send authentication data upon connection if required.",
        "protocol": "JSON messages",
    }
