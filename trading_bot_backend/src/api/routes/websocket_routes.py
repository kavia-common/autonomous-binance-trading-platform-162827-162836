"""
WebSocket routes for real-time analytics and notifications.
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.websocket.hub import WebSocketHub

router = APIRouter(tags=["WebSocket"])
hub = WebSocketHub()


@router.websocket("/ws/analytics")
# PUBLIC_INTERFACE
async def websocket_analytics(websocket: WebSocket):
    """
    WebSocket endpoint for analytics streaming.

    Usage:
    - Connect to /ws/analytics
    - The server will accept the connection.
    - In a future iteration, send auth and subscribe messages.

    Returns:
        WebSocket connection that streams analytics updates.
    """
    user_id = "placeholder"  # Will be derived from auth/token later
    await hub.connect(user_id, websocket)
    try:
        while True:
            # Placeholder: echo any received message
            data = await websocket.receive_json()
            await hub.broadcast(user_id, {"echo": data})
    except WebSocketDisconnect:
        await hub.disconnect(user_id, websocket)
