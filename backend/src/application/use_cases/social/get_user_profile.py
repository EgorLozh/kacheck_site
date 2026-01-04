from src.domain.repositories.user_repository import IUserRepository
from src.domain.repositories.follow_repository import IFollowRepository
from src.domain.entities.follow import FollowStatus
from src.application.dto.auth_dto import UserResponseDTO


class GetUserProfileUseCase:
    """Use case for getting another user's profile (requires approved follow)."""

    def __init__(
        self,
        user_repository: IUserRepository,
        follow_repository: IFollowRepository,
    ):
        self.user_repository = user_repository
        self.follow_repository = follow_repository

    def execute(self, user_id: int, current_user_id: int) -> UserResponseDTO:
        """Get user profile. Requires approved follow relationship."""
        # Check if viewing own profile
        if user_id == current_user_id:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            return UserResponseDTO(
                id=user.id,
                email=user.email,
                username=user.username,
                weight=user.weight,
                height=user.height,
            )
        
        # Check if current user has approved follow relationship with the requested user
        follow = self.follow_repository.get_by_ids(current_user_id, user_id)
        if not follow or follow.status != FollowStatus.APPROVED:
            raise ValueError("Access denied: You must be an approved follower to view this profile")
        
        # Get the user
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Return profile (without email for privacy)
        return UserResponseDTO(
            id=user.id,
            email="",  # Don't expose email for other users
            username=user.username,
            weight=user.weight,
            height=user.height,
        )

