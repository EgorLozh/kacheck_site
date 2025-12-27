from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories import TrainingTemplateRepositoryImpl
from src.application.use_cases.training_templates.create_template import CreateTemplateUseCase
from src.application.use_cases.training_templates.get_templates import GetTemplatesUseCase
from src.application.use_cases.training_templates.get_template_by_id import GetTemplateByIdUseCase
from src.application.use_cases.training_templates.update_template import UpdateTemplateUseCase
from src.application.use_cases.training_templates.delete_template import DeleteTemplateUseCase
from src.application.dto.training_template_dto import (
    CreateTemplateDTO,
    UpdateTemplateDTO,
    ImplementationTemplateDTO,
    SetTemplateDTO,
)
from src.presentation.schemas.training_template_schemas import (
    TemplateCreate,
    TemplateUpdate,
    TemplateResponse,
)
from src.presentation.api.dependencies import get_current_user_id

router = APIRouter(prefix="/training-templates", tags=["training-templates"])


def get_template_repository(db: Session = Depends(get_db)) -> TrainingTemplateRepositoryImpl:
    """Dependency to get training template repository."""
    return TrainingTemplateRepositoryImpl(db)


@router.post("", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    request: TemplateCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Create a new training template."""
    template_repository = get_template_repository(db)
    use_case = CreateTemplateUseCase(template_repository)

    try:
        # Convert schemas to DTOs
        impl_dtos = []
        for impl_schema in request.implementation_templates:
            set_dtos = [
                {
                    "order_index": st.order_index,
                    "weight": st.weight,
                    "reps": st.reps,
                }
                for st in impl_schema.set_templates
            ]
            impl_dtos.append(
                {
                    "exercise_id": impl_schema.exercise_id,
                    "order_index": impl_schema.order_index,
                    "set_templates": set_dtos,
                }
            )

        # Create DTO manually since we can't easily convert nested Pydantic models
        from src.application.dto.training_template_dto import (
            CreateTemplateDTO,
            ImplementationTemplateDTO,
            SetTemplateDTO,
        )

        impl_template_dtos = []
        for impl_data in impl_dtos:
            set_template_dtos = [
                SetTemplateDTO(**set_data) for set_data in impl_data["set_templates"]
            ]
            impl_template_dtos.append(
                ImplementationTemplateDTO(
                    exercise_id=impl_data["exercise_id"],
                    order_index=impl_data["order_index"],
                    set_templates=set_template_dtos,
                )
            )

        dto = CreateTemplateDTO(
            name=request.name,
            description=request.description,
            implementation_templates=impl_template_dtos,
        )

        result = use_case.execute(dto, current_user_id)
        return TemplateResponse(**result.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[TemplateResponse])
async def get_templates(
    include_system: bool = True,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get all training templates."""
    template_repository = get_template_repository(db)
    use_case = GetTemplatesUseCase(template_repository)

    results = use_case.execute(user_id=current_user_id, include_system=include_system)
    return [TemplateResponse(**result.__dict__) for result in results]


@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: int,
    db: Session = Depends(get_db),
):
    """Get training template by ID."""
    template_repository = get_template_repository(db)
    use_case = GetTemplateByIdUseCase(template_repository)

    result = use_case.execute(template_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")
    return TemplateResponse(**result.__dict__)


@router.put("/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: int,
    request: TemplateUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Update a training template."""
    template_repository = get_template_repository(db)
    use_case = UpdateTemplateUseCase(template_repository)

    try:
        # Convert schemas to DTOs
        impl_template_dtos = None
        if request.implementation_templates:
            impl_template_dtos = []
            for impl_data in request.implementation_templates:
                set_template_dtos = [
                    SetTemplateDTO(**set_data.dict()) for set_data in impl_data.set_templates
                ]
                impl_template_dtos.append(
                    ImplementationTemplateDTO(
                        exercise_id=impl_data.exercise_id,
                        order_index=impl_data.order_index,
                        set_templates=set_template_dtos,
                    )
                )

        dto = UpdateTemplateDTO(
            name=request.name,
            description=request.description,
            implementation_templates=impl_template_dtos,
        )

        result = use_case.execute(template_id, dto, current_user_id)
        return TemplateResponse(**result.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Delete a training template."""
    template_repository = get_template_repository(db)
    use_case = DeleteTemplateUseCase(template_repository)

    try:
        use_case.execute(template_id, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

