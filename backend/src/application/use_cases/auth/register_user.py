from datetime import datetime

from src.domain.entities.user import User
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.auth.password_service import PasswordService
from src.application.dto.auth_dto import RegisterUserDTO, UserResponseDTO


class RegisterUserUseCase:
    """Use case for user registration."""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        self.password_service = PasswordService()

    def execute(self, dto: RegisterUserDTO) -> UserResponseDTO:
        """Register a new user."""
        # Check if user already exists
        existing_user = self.user_repository.get_by_email(dto.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # Hash password
        hashed_password = self.password_service.hash_password(dto.password)

        # Create user entity
        now = datetime.utcnow()
        user = User(
            id=None,
            email=dto.email,
            username=dto.username,
            hashed_password=hashed_password,
            created_at=now,
            updated_at=now,
        )

        # Save user
        created_user = self.user_repository.create(user)

        # Return DTO
        return UserResponseDTO(
            id=created_user.id,
            email=created_user.email,
            username=created_user.username,
        )

