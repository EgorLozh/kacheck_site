from typing import List, Optional

from src.domain.repositories.exercise_repository import IExerciseRepository
from src.application.dto.exercise_dto import ExerciseResponseDTO


class GetExercisesUseCase:
    """Use case for getting exercises."""

    def __init__(self, exercise_repository: IExerciseRepository):
        self.exercise_repository = exercise_repository

    def execute(
        self, user_id: Optional[int] = None, include_system: bool = True
    ) -> List[ExerciseResponseDTO]:
        """Get all exercises."""
        exercises = self.exercise_repository.get_all(user_id=user_id, include_system=include_system)

        return [
            ExerciseResponseDTO(
                id=ex.id,
                name=str(ex.name),
                description=ex.description,
                image_path=ex.image_path,
                is_custom=ex.is_custom,
                user_id=ex.user_id,
                muscle_group_ids=ex.muscle_group_ids,
            )
            for ex in exercises
        ]





