from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories import MuscleGroupRepositoryImpl
from src.application.use_cases.muscle_groups.create_muscle_group import CreateMuscleGroupUseCase
from src.application.use_cases.muscle_groups.get_muscle_groups import GetMuscleGroupsUseCase
from src.application.dto.muscle_group_dto import CreateMuscleGroupDTO
from src.presentation.schemas.muscle_group_schemas import MuscleGroupCreate, MuscleGroupResponse

router = APIRouter(prefix="/muscle-groups", tags=["muscle-groups"])


def get_muscle_group_repository(db: Session = Depends(get_db)) -> MuscleGroupRepositoryImpl:
    """Dependency to get muscle group repository."""
    return MuscleGroupRepositoryImpl(db)


@router.post("", response_model=MuscleGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_muscle_group(
    request: MuscleGroupCreate,
    db: Session = Depends(get_db),
):
    """Create a new muscle group."""
    muscle_group_repository = get_muscle_group_repository(db)
    use_case = CreateMuscleGroupUseCase(muscle_group_repository)

    try:
        dto = CreateMuscleGroupDTO(name=request.name)
        result = use_case.execute(dto)
        return MuscleGroupResponse(**result.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[MuscleGroupResponse])
async def get_muscle_groups(
    include_system: bool = True,
    db: Session = Depends(get_db),
):
    """Get all muscle groups."""
    muscle_group_repository = get_muscle_group_repository(db)
    use_case = GetMuscleGroupsUseCase(muscle_group_repository)

    results = use_case.execute(include_system=include_system)
    return [MuscleGroupResponse(**result.__dict__) for result in results]



