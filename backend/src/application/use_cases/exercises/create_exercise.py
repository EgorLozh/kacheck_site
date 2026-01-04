from datetime import datetime

from src.domain.entities.exercise import Exercise
from src.domain.value_objects.exercise_name import ExerciseName
from src.domain.repositories.exercise_repository import IExerciseRepository
from src.application.dto.exercise_dto import CreateExerciseDTO, ExerciseResponseDTO


class CreateExerciseUseCase:
    """Use case for creating an exercise."""

    def __init__(self, exercise_repository: IExerciseRepository):
        self.exercise_repository = exercise_repository

    def execute(self, dto: CreateExerciseDTO, user_id: int) -> ExerciseResponseDTO:
        """Create a new exercise."""
        now = datetime.utcnow()
        exercise = Exercise(
            id=None,
            name=ExerciseName(dto.name),
            description=dto.description,
            image_path=dto.image_path,
            is_custom=True,
            user_id=user_id,
            muscle_group_ids=dto.muscle_group_ids,
            created_at=now,
            updated_at=now,
        )

        created_exercise = self.exercise_repository.create(exercise)

        return ExerciseResponseDTO(
            id=created_exercise.id,
            name=str(created_exercise.name),
            description=created_exercise.description,
            image_path=created_exercise.image_path,
            is_custom=created_exercise.is_custom,
            user_id=created_exercise.user_id,
            muscle_group_ids=created_exercise.muscle_group_ids,
        )





