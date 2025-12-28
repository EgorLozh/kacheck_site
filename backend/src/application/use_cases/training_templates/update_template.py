from src.domain.entities.training_template import TrainingTemplate
from src.domain.entities.implementation_template import ImplementationTemplate
from src.domain.entities.set_template import SetTemplate
from src.domain.repositories.training_template_repository import ITrainingTemplateRepository
from src.application.dto.training_template_dto import (
    UpdateTemplateDTO,
    TemplateResponseDTO,
    ImplementationTemplateDTO,
    SetTemplateDTO,
)


class UpdateTemplateUseCase:
    """Use case for updating a training template."""

    def __init__(self, template_repository: ITrainingTemplateRepository):
        self.template_repository = template_repository

    def execute(self, template_id: int, dto: UpdateTemplateDTO, user_id: int) -> TemplateResponseDTO:
        """Update a training template."""
        # Get existing template
        template = self.template_repository.get_by_id(template_id)
        if not template:
            raise ValueError(f"Template with id {template_id} not found")

        # Check ownership
        if template.user_id != user_id:
            raise ValueError("You don't have permission to update this template")

        # Update fields
        if dto.name is not None:
            template.name = dto.name
        if dto.description is not None:
            template.description = dto.description
        if dto.implementation_templates is not None:
            # Convert DTOs to domain entities
            impl_templates = []
            for impl_dto in dto.implementation_templates:
                set_templates = [
                    SetTemplate(
                        id=None,
                        implementation_template_id=0,
                        order_index=set_dto.order_index,
                        weight=set_dto.weight,
                        reps=set_dto.reps,
                    )
                    for set_dto in impl_dto.set_templates
                ]
                impl_templates.append(
                    ImplementationTemplate(
                        id=None,
                        training_template_id=template.id,
                        exercise_id=impl_dto.exercise_id,
                        order_index=impl_dto.order_index,
                        set_templates=set_templates,
                    )
                )
            template.implementation_templates = impl_templates

        updated_template = self.template_repository.update(template)
        return self._to_dto(updated_template)

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



