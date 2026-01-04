from typing import List
from src.domain.repositories.user_repository import IUserRepository
from src.domain.entities.user import User


class SearchUsersUseCase:
    """Use case for searching users by username."""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, username_query: str, limit: int = 20, exclude_user_id: int = None) -> List[User]:
        """Search users by username, optionally excluding a specific user."""
        users = self.user_repository.search_by_username(username_query, limit)
        
        # Exclude the current user from results
        if exclude_user_id is not None:
            users = [user for user in users if user.id != exclude_user_id]
        
        return users

