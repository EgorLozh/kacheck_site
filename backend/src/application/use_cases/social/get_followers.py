from typing import List
from src.domain.repositories.follow_repository import IFollowRepository
from src.domain.entities.follow import Follow


class GetFollowersUseCase:
    """Use case for getting followers of a user."""

    def __init__(self, follow_repository: IFollowRepository):
        self.follow_repository = follow_repository

    def execute(self, user_id: int) -> List[Follow]:
        """Get all followers of a user."""
        return self.follow_repository.get_followers(user_id)


