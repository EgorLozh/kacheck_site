from datetime import datetime

from src.domain.repositories.training_repository import ITrainingRepository
from src.domain.repositories.training_template_repository import ITrainingTemplateRepository
from src.domain.services.template_service import TemplateService
from src.application.dto.training_dto import TrainingResponseDTO, ImplementationDTO, SetDTO


class CreateTrainingFromTemplateUseCase:
    """Use case for creating a training from a template."""

    def __init__(
        self,
        training_repository: ITrainingRepository,
        template_repository: ITrainingTemplateRepository,
    ):
        self.training_repository = training_repository
        self.template_repository = template_repository

    def execute(self, template_id: int, user_id: int, date_time: datetime) -> TrainingResponseDTO:
        """Create a training from a template."""
        # Get template
        template = self.template_repository.get_by_id(template_id)
        if not template:
            raise ValueError(f"Template with id {template_id} not found")

        # Create training from template using domain service
        training = TemplateService.create_training_from_template(template, user_id, date_time)

        # Save training
        created_training = self.training_repository.create(training)

        # Convert to DTO
        return self._to_dto(created_training)

    @staticmethod
    def _to_dto(training) -> TrainingResponseDTO:
        """Convert domain entity to DTO."""
        impl_dtos = []
        for impl in training.implementations:
            set_dtos = [
                SetDTO(
                    order_index=s.order_index,
                    weight=float(s.weight.value),
                    reps=int(s.reps.value),
                    rest_time=int(s.rest_time.value) if s.rest_time else None,
                    duration=int(s.duration.value) if s.duration else None,
                    rpe=int(s.rpe.value) if s.rpe else None,
                )
                for s in impl.sets
            ]
            impl_dtos.append(
                ImplementationDTO(
                    exercise_id=impl.exercise_id,
                    order_index=impl.order_index,
                    sets=set_dtos,
                )
            )

        return TrainingResponseDTO(
            id=training.id,
            user_id=training.user_id,
            training_template_id=training.training_template_id,
            date_time=training.date_time,
            duration=training.duration,
            notes=training.notes,
            status=training.status,
            implementations=impl_dtos,
        )

