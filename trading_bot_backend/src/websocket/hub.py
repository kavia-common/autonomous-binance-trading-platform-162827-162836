"""
WebSocket hub for real-time analytics and notifications.
"""
from typing import Dict, Set
from fastapi import WebSocket


class WebSocketHub:
    """Tracks active WebSocket connections per user."""

    def __init__(self) -> None:
        """Initialize internal maps."""
        self._connections: Dict[str, Set[WebSocket]] = {}

    # PUBLIC_INTERFACE
    async def connect(self, user_id: str, websocket: WebSocket) -> None:
        """Accept and register a WebSocket for a user."""
        await websocket.accept()
        self._connections.setdefault(user_id, set()).add(websocket)

    # PUBLIC_INTERFACE
    async def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        """Remove a WebSocket from a user."""
        conns = self._connections.get(user_id)
        if conns and websocket in conns:
            conns.remove(websocket)

    # PUBLIC_INTERFACE
    async def broadcast(self, user_id: str, message: dict) -> None:
        """Broadcast a message to all websockets for a user."""
        for ws in self._connections.get(user_id, set()):
            await ws.send_json(message)
