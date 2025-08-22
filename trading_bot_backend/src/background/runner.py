"""
Background tasks runner skeleton for strategy evaluation and periodic jobs.
"""
from typing import Callable, Any


class BackgroundRunner:
    """Manages registration and execution of background jobs."""

    def __init__(self) -> None:
        """Initialize background runner with internal registry."""
        self._jobs: list[Callable[[], Any]] = []

    # PUBLIC_INTERFACE
    def register(self, job: Callable[[], Any]) -> None:
        """Register a background job."""
        self._jobs.append(job)

    # PUBLIC_INTERFACE
    def start(self) -> None:
        """Start background jobs (placeholder)."""
        # Will be implemented with asyncio/background tasks.
        return None

    # PUBLIC_INTERFACE
    def stop(self) -> None:
        """Stop background jobs (placeholder)."""
        return None
