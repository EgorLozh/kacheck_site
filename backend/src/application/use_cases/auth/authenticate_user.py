from datetime import timedelta

from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.auth.password_service import PasswordService
from src.infrastructure.auth.jwt_service import JWTService
from src.infrastructure.settings import settings
from src.application.dto.auth_dto import LoginUserDTO, TokenResponseDTO


class AuthenticateUserUseCase:
    """Use case for user authentication."""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        self.password_service = PasswordService()
        self.jwt_service = JWTService()

    def execute(self, dto: LoginUserDTO) -> TokenResponseDTO:
        """Authenticate user and return access token."""
        # Get user by email
        user = self.user_repository.get_by_email(dto.email)
        if not user:
            raise ValueError("Invalid email or password")

        # Verify password
        if not self.password_service.verify_password(dto.password, user.hashed_password):
            raise ValueError("Invalid email or password")

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.jwt_service.create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires,
        )

        return TokenResponseDTO(access_token=access_token, token_type="bearer")

