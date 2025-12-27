from typing import Optional

from src.domain.repositories.exercise_repository import IExerciseRepository
from src.application.dto.exercise_dto import ExerciseResponseDTO


class GetExerciseByIdUseCase:
    """Use case for getting an exercise by ID."""

    def __init__(self, exercise_repository: IExerciseRepository):
        self.exercise_repository = exercise_repository

    def execute(self, exercise_id: int) -> Optional[ExerciseResponseDTO]:
        """Get exercise by ID."""
        exercise = self.exercise_repository.get_by_id(exercise_id)
        if not exercise:
            return None

        return ExerciseResponseDTO(
            id=exercise.id,
            name=str(exercise.name),
            description=exercise.description,
            image_path=exercise.image_path,
            is_custom=exercise.is_custom,
            user_id=exercise.user_id,
            muscle_group_ids=exercise.muscle_group_ids,
        )

