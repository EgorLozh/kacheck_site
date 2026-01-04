from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.follow import Follow, FollowStatus


class IFollowRepository(ABC):
    """Interface for Follow repository (Port)."""

    @abstractmethod
    def create(self, follow: Follow) -> Follow:
        """Create a new follow relationship."""
        pass

    @abstractmethod
    def delete(self, follower_id: int, following_id: int) -> None:
        """Delete a follow relationship."""
        pass

    @abstractmethod
    def get_by_ids(self, follower_id: int, following_id: int) -> Optional[Follow]:
        """Get follow relationship by follower and following IDs."""
        pass

    @abstractmethod
    def get_followers(self, user_id: int) -> List[Follow]:
        """Get all users following a user."""
        pass

    @abstractmethod
    def get_following(self, user_id: int) -> List[Follow]:
        """Get all users a user is following."""
        pass

    @abstractmethod
    def update_status(self, follower_id: int, following_id: int, status: FollowStatus) -> Optional[Follow]:
        """Update follow request status."""
        pass

    @abstractmethod
    def get_following_approved(self, user_id: int) -> List[Follow]:
        """Get all users a user is following with approved status."""
        pass


