from typing import Optional

from src.domain.repositories.exercise_repository import IExerciseRepository
from src.application.dto.exercise_dto import ExerciseResponseDTO


class GetExerciseByIdUseCase:
    """Use case for getting an exercise by ID."""

    def __init__(self, exercise_repository: IExerciseRepository):
        self.exercise_repository = exercise_repository

    def execute(self, exercise_id: int, user_id: Optional[int] = None) -> Optional[ExerciseResponseDTO]:
        """Get exercise by ID."""
        exercise = self.exercise_repository.get_by_id(exercise_id)
        if not exercise:
            return None

        # Check access: user can only see their own exercises or system exercises
        if user_id is not None:
            if exercise.is_custom:
                # Custom exercises must belong to the user
                if exercise.user_id != user_id:
                    return None
            else:
                # System exercises (is_custom=False) should have user_id=None and are available to everyone
                # But check for data integrity: system exercises should not have user_id set
                if exercise.user_id is not None:
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


