from src.domain.repositories.follow_repository import IFollowRepository


class UnfollowUserUseCase:
    """Use case for unfollowing a user."""

    def __init__(self, follow_repository: IFollowRepository):
        self.follow_repository = follow_repository

    def execute(self, follower_id: int, following_id: int) -> None:
        """Unfollow a user."""
        # Check if following
        existing = self.follow_repository.get_by_ids(follower_id, following_id)
        if not existing:
            raise ValueError("Not following this user")

        self.follow_repository.delete(follower_id, following_id)


