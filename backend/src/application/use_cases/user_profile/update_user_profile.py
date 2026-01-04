from datetime import datetime

from src.domain.entities.user import User
from src.domain.repositories.user_repository import IUserRepository
from src.application.dto.user_body_metric_dto import UpdateUserProfileDTO
from src.application.dto.auth_dto import UserResponseDTO


class UpdateUserProfileUseCase:
    """Use case for updating user profile (current weight and height)."""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, dto: UpdateUserProfileDTO, user_id: int) -> UserResponseDTO:
        """Update user profile."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Update only provided fields
        if dto.weight is not None:
            user.weight = dto.weight
        if dto.height is not None:
            user.height = dto.height

        user.updated_at = datetime.utcnow()

        updated_user = self.user_repository.update(user)

        return UserResponseDTO(
            id=updated_user.id,
            email=updated_user.email,
            username=updated_user.username,
            weight=updated_user.weight,
            height=updated_user.height,
        )




