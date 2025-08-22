"""
User repository interface skeleton.
"""
from typing import Optional, List
from src.domain.models import User
from src.repositories.base import Repository


class UserRepository(Repository[User]):
    """User repository implementing base methods (skeleton)."""

    # PUBLIC_INTERFACE
    def get(self, item_id: str) -> Optional[User]:
        """Fetch a user by ID."""
        return None

    # PUBLIC_INTERFACE
    def list(self) -> List[User]:
        """List all users."""
        return []

    # PUBLIC_INTERFACE
    def create(self, item: User) -> User:
        """Create a user."""
        return item

    # PUBLIC_INTERFACE
    def update(self, item_id: str, item: User) -> User:
        """Update a user."""
        return item

    # PUBLIC_INTERFACE
    def delete(self, item_id: str) -> None:
        """Delete a user."""
        return None
