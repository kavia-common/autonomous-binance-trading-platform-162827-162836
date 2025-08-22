"""
Health and status routes.
"""
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/", summary="Health Check", description="Return basic health information.", operation_id="health_check")
# PUBLIC_INTERFACE
def health_check() -> dict:
    """Return health status."""
    return {"status": "ok"}
