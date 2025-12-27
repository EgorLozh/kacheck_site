from src.domain.entities.exercise import Exercise
from src.domain.value_objects.exercise_name import ExerciseName
from src.domain.repositories.exercise_repository import IExerciseRepository
from src.application.dto.exercise_dto import UpdateExerciseDTO, ExerciseResponseDTO


class UpdateExerciseUseCase:
    """Use case for updating an exercise."""

    def __init__(self, exercise_repository: IExerciseRepository):
        self.exercise_repository = exercise_repository

    def execute(self, exercise_id: int, dto: UpdateExerciseDTO, user_id: int) -> ExerciseResponseDTO:
        """Update an exercise."""
        # Get existing exercise
        exercise = self.exercise_repository.get_by_id(exercise_id)
        if not exercise:
            raise ValueError(f"Exercise with id {exercise_id} not found")

        # Check ownership for custom exercises
        if exercise.is_custom and exercise.user_id != user_id:
            raise ValueError("You don't have permission to update this exercise")

        # Update fields
        if dto.name is not None:
            exercise.name = ExerciseName(dto.name)
        if dto.description is not None:
            exercise.description = dto.description
        if dto.image_path is not None:
            exercise.image_path = dto.image_path
        if dto.muscle_group_ids is not None:
            exercise.muscle_group_ids = dto.muscle_group_ids

        updated_exercise = self.exercise_repository.update(exercise)

        return ExerciseResponseDTO(
            id=updated_exercise.id,
            name=str(updated_exercise.name),
            description=updated_exercise.description,
            image_path=updated_exercise.image_path,
            is_custom=updated_exercise.is_custom,
            user_id=updated_exercise.user_id,
            muscle_group_ids=updated_exercise.muscle_group_ids,
        )

