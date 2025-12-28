from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories import TrainingRepositoryImpl, TrainingTemplateRepositoryImpl
from src.application.use_cases.trainings.create_training import CreateTrainingUseCase
from src.application.use_cases.trainings.get_training_by_id import GetTrainingByIdUseCase
from src.application.use_cases.trainings.update_training import UpdateTrainingUseCase
from src.application.use_cases.trainings.delete_training import DeleteTrainingUseCase
from src.application.use_cases.trainings.create_training_from_template import (
    CreateTrainingFromTemplateUseCase,
)
from src.application.use_cases.trainings.get_last_exercise_implementation import (
    GetLastExerciseImplementationUseCase,
)
from src.application.dto.training_dto import CreateTrainingDTO, UpdateTrainingDTO, ImplementationDTO, SetDTO
from src.presentation.schemas.training_schemas import (
    TrainingCreate,
    TrainingUpdate,
    TrainingResponse,
    ImplementationBase,
    SetBase,
)
from src.presentation.api.dependencies import get_current_user_id

router = APIRouter(prefix="/trainings", tags=["trainings"])


def dto_to_response(dto) -> TrainingResponse:
    """Convert TrainingResponseDTO to TrainingResponse Pydantic schema."""
    impl_schemas = []
    for impl_dto in dto.implementations:
        set_schemas = [
            SetBase(
                order_index=st.order_index,
                weight=st.weight,
                reps=st.reps,
                rest_time=st.rest_time,
                duration=st.duration,
                rpe=st.rpe,
            )
            for st in impl_dto.sets
        ]
        impl_schemas.append(
            ImplementationBase(
                exercise_id=impl_dto.exercise_id,
                order_index=impl_dto.order_index,
                sets=set_schemas,
            )
        )
    
    return TrainingResponse(
        id=dto.id,
        user_id=dto.user_id,
        training_template_id=dto.training_template_id,
        date_time=dto.date_time,
        duration=dto.duration,
        notes=dto.notes,
        status=dto.status,
        implementations=impl_schemas,
    )


def get_training_repository(db: Session = Depends(get_db)) -> TrainingRepositoryImpl:
    """Dependency to get training repository."""
    return TrainingRepositoryImpl(db)


@router.post("", response_model=TrainingResponse, status_code=status.HTTP_201_CREATED)
async def create_training(
    request: TrainingCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Create a new training."""
    training_repository = get_training_repository(db)
    use_case = CreateTrainingUseCase(training_repository)

    try:
        # Convert schemas to DTOs
        impl_dtos = []
        if request.implementations:
            for impl_schema in request.implementations:
                set_dtos = [
                    SetDTO(
                        order_index=st.order_index,
                        weight=st.weight,
                        reps=st.reps,
                        rest_time=st.rest_time,
                        duration=st.duration,
                        rpe=st.rpe,
                    )
                    for st in impl_schema.sets
                ]
                impl_dtos.append(
                    ImplementationDTO(
                        exercise_id=impl_schema.exercise_id,
                        order_index=impl_schema.order_index,
                        sets=set_dtos,
                    )
                )

        dto = CreateTrainingDTO(
            date_time=request.date_time,
            training_template_id=request.training_template_id,
            implementations=impl_dtos if impl_dtos else None,
            duration=request.duration,
            notes=request.notes,
            status=request.status,
        )

        result = use_case.execute(dto, current_user_id)
        return dto_to_response(result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[TrainingResponse])
async def get_trainings(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get all trainings for current user."""
    training_repository = get_training_repository(db)
    trainings = training_repository.get_all(
        user_id=current_user_id, start_date=start_date, end_date=end_date
    )

    # Convert to DTOs
    from src.application.use_cases.trainings.get_training_by_id import GetTrainingByIdUseCase

    results = []
    for training in trainings:
        dto = GetTrainingByIdUseCase._to_dto(training)
        results.append(dto)

    return [dto_to_response(result) for result in results]


@router.get("/{training_id}", response_model=TrainingResponse)
async def get_training(
    training_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get training by ID."""
    training_repository = get_training_repository(db)
    use_case = GetTrainingByIdUseCase(training_repository)

    result = use_case.execute(training_id, current_user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Training not found")
    return dto_to_response(result)


@router.put("/{training_id}", response_model=TrainingResponse)
async def update_training(
    training_id: int,
    request: TrainingUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Update a training."""
    training_repository = get_training_repository(db)
    use_case = UpdateTrainingUseCase(training_repository)

    try:
        # Convert schemas to DTOs
        impl_dtos = None
        if request.implementations:
            impl_dtos = []
            for impl_schema in request.implementations:
                set_dtos = [
                    SetDTO(
                        order_index=st.order_index,
                        weight=st.weight,
                        reps=st.reps,
                        rest_time=st.rest_time,
                        duration=st.duration,
                        rpe=st.rpe,
                    )
                    for st in impl_schema.sets
                ]
                impl_dtos.append(
                    ImplementationDTO(
                        exercise_id=impl_schema.exercise_id,
                        order_index=impl_schema.order_index,
                        sets=set_dtos,
                    )
                )

        dto = UpdateTrainingDTO(
            date_time=request.date_time,
            implementations=impl_dtos,
            duration=request.duration,
            notes=request.notes,
            status=request.status,
        )

        result = use_case.execute(training_id, dto, current_user_id)
        return dto_to_response(result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{training_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_training(
    training_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Delete a training."""
    training_repository = get_training_repository(db)
    use_case = DeleteTrainingUseCase(training_repository)

    try:
        use_case.execute(training_id, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/from-template/{template_id}", response_model=TrainingResponse, status_code=status.HTTP_201_CREATED)
async def create_training_from_template(
    template_id: int,
    date_time: datetime,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Create a training from a template."""
    training_repository = get_training_repository(db)
    template_repository = TrainingTemplateRepositoryImpl(db)
    use_case = CreateTrainingFromTemplateUseCase(training_repository, template_repository)

    try:
        result = use_case.execute(template_id, current_user_id, date_time)
        return dto_to_response(result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/last-exercise/{exercise_id}", response_model=Optional[ImplementationBase])
async def get_last_exercise_implementation(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get last implementation of an exercise from completed training."""
    training_repository = get_training_repository(db)
    use_case = GetLastExerciseImplementationUseCase(training_repository)

    result = use_case.execute(exercise_id, current_user_id)
    if not result:
        return None

    set_schemas = [
        SetBase(
            order_index=st.order_index,
            weight=st.weight,
            reps=st.reps,
            rest_time=st.rest_time,
            duration=st.duration,
            rpe=st.rpe,
        )
        for st in result.sets
    ]

    return ImplementationBase(
        exercise_id=result.exercise_id,
        order_index=result.order_index,
        sets=set_schemas,
    )

