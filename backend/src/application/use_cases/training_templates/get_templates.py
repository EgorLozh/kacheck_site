from typing import List, Optional

from src.domain.repositories.training_template_repository import ITrainingTemplateRepository
from src.application.dto.training_template_dto import TemplateResponseDTO, ImplementationTemplateDTO, SetTemplateDTO


class GetTemplatesUseCase:
    """Use case for getting training templates."""

    def __init__(self, template_repository: ITrainingTemplateRepository):
        self.template_repository = template_repository

    def execute(
        self, user_id: Optional[int] = None, include_system: bool = True
    ) -> List[TemplateResponseDTO]:
        """Get all training templates."""
        templates = self.template_repository.get_all(user_id=user_id, include_system=include_system)

        return [self._to_dto(t) for t in templates]

    @staticmethod
    def _to_dto(template) -> TemplateResponseDTO:
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

