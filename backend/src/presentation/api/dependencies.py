from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories import UserRepositoryImpl
from src.infrastructure.auth.jwt_service import JWTService
from src.domain.repositories.user_repository import IUserRepository

security = HTTPBearer()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    """Dependency to get user repository."""
    return UserRepositoryImpl(db)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repository: IUserRepository = Depends(get_user_repository),
) -> int:
    """Get current user ID from JWT token."""
    jwt_service = JWTService()
    token = credentials.credentials
    payload = jwt_service.verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    # Verify user exists
    user = user_repository.get_by_id(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return int(user_id)
