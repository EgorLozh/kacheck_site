from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories import UserRepositoryImpl
from src.application.use_cases.auth.register_user import RegisterUserUseCase
from src.application.use_cases.auth.authenticate_user import AuthenticateUserUseCase
from src.application.dto.auth_dto import RegisterUserDTO, LoginUserDTO
from src.presentation.schemas.auth_schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    """Dependency to get user repository."""
    return UserRepositoryImpl(db)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    """Register a new user."""
    user_repository = get_user_repository(db)
    use_case = RegisterUserUseCase(user_repository)

    try:
        dto = RegisterUserDTO(
            email=request.email,
            username=request.username,
            password=request.password,
        )
        result = use_case.execute(dto)
        return UserResponse(**result.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    """Login user and get access token."""
    user_repository = get_user_repository(db)
    use_case = AuthenticateUserUseCase(user_repository)

    try:
        dto = LoginUserDTO(email=request.email, password=request.password)
        result = use_case.execute(dto)
        return TokenResponse(**result.__dict__)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

