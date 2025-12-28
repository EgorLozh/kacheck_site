from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories import ExerciseRepositoryImpl
from src.application.use_cases.exercises.create_exercise import CreateExerciseUseCase
from src.application.use_cases.exercises.get_exercises import GetExercisesUseCase
from src.application.use_cases.exercises.get_exercise_by_id import GetExerciseByIdUseCase
from src.application.use_cases.exercises.update_exercise import UpdateExerciseUseCase
from src.application.use_cases.exercises.delete_exercise import DeleteExerciseUseCase
from src.application.dto.exercise_dto import CreateExerciseDTO, UpdateExerciseDTO
from src.presentation.schemas.exercise_schemas import ExerciseCreate, ExerciseUpdate, ExerciseResponse
from src.presentation.api.dependencies import get_current_user_id

router = APIRouter(prefix="/exercises", tags=["exercises"])


def get_exercise_repository(db: Session = Depends(get_db)) -> ExerciseRepositoryImpl:
    """Dependency to get exercise repository."""
    return ExerciseRepositoryImpl(db)


@router.post("", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(
    request: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Create a new exercise."""
    exercise_repository = get_exercise_repository(db)
    use_case = CreateExerciseUseCase(exercise_repository)

    try:
        dto = CreateExerciseDTO(
            name=request.name,
            description=request.description,
            muscle_group_ids=request.muscle_group_ids,
            image_path=request.image_path,
        )
        result = use_case.execute(dto, user_id=current_user_id)
        return ExerciseResponse(**result.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[ExerciseResponse])
async def get_exercises(
    include_system: bool = True,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get all exercises."""
    exercise_repository = get_exercise_repository(db)
    use_case = GetExercisesUseCase(exercise_repository)

    results = use_case.execute(user_id=current_user_id, include_system=include_system)
    return [ExerciseResponse(**result.__dict__) for result in results]


@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get exercise by ID."""
    exercise_repository = get_exercise_repository(db)
    use_case = GetExerciseByIdUseCase(exercise_repository)

    result = use_case.execute(exercise_id, user_id=current_user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return ExerciseResponse(**result.__dict__)


@router.put("/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: int,
    request: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Update an exercise."""
    exercise_repository = get_exercise_repository(db)
    use_case = UpdateExerciseUseCase(exercise_repository)

    try:
        dto = UpdateExerciseDTO(
            name=request.name,
            description=request.description,
            muscle_group_ids=request.muscle_group_ids,
            image_path=request.image_path,
        )
        result = use_case.execute(exercise_id, dto, current_user_id)
        return ExerciseResponse(**result.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Delete an exercise."""
    exercise_repository = get_exercise_repository(db)
    use_case = DeleteExerciseUseCase(exercise_repository)

    try:
        use_case.execute(exercise_id, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

