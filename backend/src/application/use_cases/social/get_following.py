from typing import List
from src.domain.repositories.follow_repository import IFollowRepository
from src.domain.entities.follow import Follow


class GetFollowingUseCase:
    """Use case for getting users that a user is following."""

    def __init__(self, follow_repository: IFollowRepository):
        self.follow_repository = follow_repository

    def execute(self, user_id: int) -> List[Follow]:
        """Get all users that a user is following."""
        return self.follow_repository.get_following(user_id)


