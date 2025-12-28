from src.domain.repositories.user_repository import IUserRepository
from src.application.dto.auth_dto import UserResponseDTO


class GetUserProfileUseCase:
    """Use case for getting user profile."""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> UserResponseDTO:
        """Get user profile."""
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

