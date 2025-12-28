from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories import UserRepositoryImpl, UserBodyMetricRepositoryImpl
from src.application.use_cases.user_profile.create_body_metric import CreateBodyMetricUseCase
from src.application.use_cases.user_profile.get_body_metrics import GetBodyMetricsUseCase
from src.application.use_cases.user_profile.get_user_profile import GetUserProfileUseCase
from src.application.use_cases.user_profile.update_user_profile import UpdateUserProfileUseCase
from src.application.dto.user_body_metric_dto import CreateBodyMetricDTO, UpdateUserProfileDTO
from src.presentation.schemas.user_profile_schemas import (
    CreateBodyMetricRequest,
    BodyMetricResponse,
    UpdateUserProfileRequest,
)
from src.presentation.schemas.auth_schemas import UserResponse
from src.presentation.api.dependencies import get_current_user_id

router = APIRouter(prefix="/user/profile", tags=["user-profile"])


def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    """Dependency to get user repository."""
    return UserRepositoryImpl(db)


def get_body_metric_repository(db: Session = Depends(get_db)) -> UserBodyMetricRepositoryImpl:
    """Dependency to get body metric repository."""
    return UserBodyMetricRepositoryImpl(db)


@router.get("", response_model=UserResponse)
async def get_profile(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get current user profile."""
    user_repository = get_user_repository(db)
    use_case = GetUserProfileUseCase(user_repository)

    try:
        result = use_case.execute(current_user_id)
        return UserResponse(**result.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("", response_model=UserResponse)
async def update_profile(
    request: UpdateUserProfileRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Update current user profile (weight and height)."""
    user_repository = get_user_repository(db)
    use_case = UpdateUserProfileUseCase(user_repository)

    try:
        dto = UpdateUserProfileDTO(weight=request.weight, height=request.height)
        result = use_case.execute(dto, current_user_id)
        return UserResponse(**result.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/body-metrics", response_model=BodyMetricResponse, status_code=status.HTTP_201_CREATED)
async def create_body_metric(
    request: CreateBodyMetricRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Add a new body metric entry (weight and/or height measurement)."""
    body_metric_repository = get_body_metric_repository(db)
    user_repository = get_user_repository(db)
    use_case = CreateBodyMetricUseCase(body_metric_repository, user_repository)

    try:
        dto = CreateBodyMetricDTO(
            weight=request.weight,
            height=request.height,
            date=request.date,
        )
        result = use_case.execute(dto, current_user_id)
        return BodyMetricResponse(**result.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/body-metrics", response_model=List[BodyMetricResponse])
async def get_body_metrics(
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get body metrics history for current user."""
    body_metric_repository = get_body_metric_repository(db)
    use_case = GetBodyMetricsUseCase(body_metric_repository)

    try:
        results = use_case.execute(
            user_id=current_user_id,
            start_date=start_date,
            end_date=end_date,
        )
        return [BodyMetricResponse(**result.__dict__) for result in results]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

