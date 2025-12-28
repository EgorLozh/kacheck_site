from abc import ABC, abstractmethod
from typing import Optional

from ..entities.user import User


class IUserRepository(ABC):
    """Interface for User repository (Port)."""

    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Update user."""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        """Delete user."""
        pass


