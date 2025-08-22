from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import api_router, openapi_tags
from src.api.routes.health import router as health_router
from src.api.routes.auth import router as auth_router
from src.api.routes.trading import router as trading_router
from src.api.routes.strategies import router as strategies_router
from src.api.routes.analytics import router as analytics_router
from src.api.routes.websocket_routes import router as ws_router

from src.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Autonomous Binance Trading Backend",
    description="Backend API for orchestrating trading operations, integrating with Binance API, managing AI strategies, and handling Demo/Live trading modes.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", summary="Health Check", tags=["Health"])
# PUBLIC_INTERFACE
def health_check() -> dict:
    """Return service health status."""
    return {"message": "Healthy"}


# Include routers
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(trading_router)
api_router.include_router(strategies_router)
api_router.include_router(analytics_router)
api_router.include_router(ws_router)
app.include_router(api_router)


@app.on_event("startup")
async def on_startup() -> None:
    """Application startup hook."""
    # Placeholder for initializing database connections, background runner, etc.
    return None


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Application shutdown hook."""
    # Placeholder for graceful shutdown/cleanup.
    return None
