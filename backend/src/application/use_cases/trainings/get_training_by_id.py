from typing import Optional

from src.domain.repositories.training_repository import ITrainingRepository
from src.application.dto.training_dto import TrainingResponseDTO, ImplementationDTO, SetDTO


class GetTrainingByIdUseCase:
    """Use case for getting a training by ID."""

    def __init__(self, training_repository: ITrainingRepository):
        self.training_repository = training_repository

    def execute(self, training_id: int, user_id: int) -> Optional[TrainingResponseDTO]:
        """Get training by ID."""
        training = self.training_repository.get_by_id(training_id)
        if not training:
            return None

        # Check ownership
        if training.user_id != user_id:
            return None  # Don't reveal that training exists

        return self._to_dto(training)

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
            created_at=training.created_at,
            share_token=training.share_token,
            implementations=impl_dtos,
        )




