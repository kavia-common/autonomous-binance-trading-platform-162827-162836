"""
Repository base interfaces and common patterns.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Generic repository interface."""

    @abstractmethod
    # PUBLIC_INTERFACE
    def get(self, item_id: str) -> Optional[T]:
        """Return an item by ID."""
        raise NotImplementedError

    @abstractmethod
    # PUBLIC_INTERFACE
    def list(self) -> List[T]:
        """Return all items."""
        raise NotImplementedError

    @abstractmethod
    # PUBLIC_INTERFACE
    def create(self, item: T) -> T:
        """Create and return an item."""
        raise NotImplementedError

    @abstractmethod
    # PUBLIC_INTERFACE
    def update(self, item_id: str, item: T) -> T:
        """Update and return the item."""
        raise NotImplementedError

    @abstractmethod
    # PUBLIC_INTERFACE
    def delete(self, item_id: str) -> None:
        """Delete an item by ID."""
        raise NotImplementedError
