from typing import Optional
from src.domain.repositories.training_repository import ITrainingRepository
from src.application.dto.training_dto import SetDTO, ImplementationDTO


class GetLastExerciseImplementationUseCase:
    """Use case for getting last exercise implementation."""

    def __init__(self, training_repository: ITrainingRepository):
        self.training_repository = training_repository

    def execute(self, exercise_id: int, user_id: int) -> Optional[ImplementationDTO]:
        """Get last implementation of an exercise."""
        implementation = self.training_repository.get_last_exercise_implementation(
            user_id, exercise_id
        )

        if not implementation:
            return None

        set_dtos = [
            SetDTO(
                order_index=s.order_index,
                weight=float(s.weight.value),
                reps=int(s.reps.value),
                rest_time=int(s.rest_time.value) if s.rest_time else None,
                duration=int(s.duration.value) if s.duration else None,
                rpe=int(s.rpe.value) if s.rpe else None,
            )
            for s in implementation.sets
        ]

        return ImplementationDTO(
            exercise_id=implementation.exercise_id,
            order_index=implementation.order_index,
            sets=set_dtos,
        )

