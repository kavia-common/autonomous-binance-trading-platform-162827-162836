"""
FastAPI router setup and OpenAPI tags.
"""
from fastapi import APIRouter

openapi_tags = [
    {"name": "Health", "description": "Health and service status."},
    {"name": "Auth", "description": "Authentication and user account management."},
    {"name": "Trading", "description": "Trading actions, orders, and mode switching."},
    {"name": "Strategies", "description": "Strategy configuration management."},
    {"name": "Analytics", "description": "AI performance analytics and metrics."},
    {"name": "WebSocket", "description": "Real-time analytics and notifications via WebSocket."},
]

api_router = APIRouter()
