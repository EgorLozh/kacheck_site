from datetime import datetime

from src.domain.entities.training_template import TrainingTemplate
from src.domain.entities.implementation_template import ImplementationTemplate
from src.domain.entities.set_template import SetTemplate
from src.domain.repositories.training_template_repository import ITrainingTemplateRepository
from src.application.dto.training_template_dto import (
    CreateTemplateDTO,
    TemplateResponseDTO,
    ImplementationTemplateDTO,
    SetTemplateDTO,
)


class CreateTemplateUseCase:
    """Use case for creating a training template."""

    def __init__(self, template_repository: ITrainingTemplateRepository):
        self.template_repository = template_repository

    def execute(self, dto: CreateTemplateDTO, user_id: int) -> TemplateResponseDTO:
        """Create a new training template."""
        now = datetime.utcnow()

        # Convert DTOs to domain entities
        impl_templates = []
        for impl_dto in dto.implementation_templates:
            set_templates = [
                SetTemplate(
                    id=None,
                    implementation_template_id=0,  # Will be set when saved
                    order_index=set_dto.order_index,
                    weight=set_dto.weight,
                    reps=set_dto.reps,
                )
                for set_dto in impl_dto.set_templates
            ]
            impl_templates.append(
                ImplementationTemplate(
                    id=None,
                    training_template_id=0,  # Will be set when saved
                    exercise_id=impl_dto.exercise_id,
                    order_index=impl_dto.order_index,
                    set_templates=set_templates,
                )
            )

        template = TrainingTemplate(
            id=None,
            name=dto.name,
            description=dto.description,
            user_id=user_id,
            implementation_templates=impl_templates,
            created_at=now,
            updated_at=now,
        )

        created_template = self.template_repository.create(template)
        return self._to_dto(created_template)

    @staticmethod
    def _to_dto(template: TrainingTemplate) -> TemplateResponseDTO:
        """Convert domain entity to DTO."""
        impl_dtos = []
        for impl_template in template.implementation_templates:
            set_dtos = [
                SetTemplateDTO(
                    order_index=st.order_index,
                    weight=st.weight,
                    reps=st.reps,
                )
                for st in impl_template.set_templates
            ]
            impl_dtos.append(
                ImplementationTemplateDTO(
                    exercise_id=impl_template.exercise_id,
                    order_index=impl_template.order_index,
                    set_templates=set_dtos,
                )
            )

        return TemplateResponseDTO(
            id=template.id,
            name=template.name,
            description=template.description,
            user_id=template.user_id,
            implementation_templates=impl_dtos,
        )

