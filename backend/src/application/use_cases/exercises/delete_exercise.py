from src.domain.repositories.exercise_repository import IExerciseRepository


class DeleteExerciseUseCase:
    """Use case for deleting an exercise."""

    def __init__(self, exercise_repository: IExerciseRepository):
        self.exercise_repository = exercise_repository

    def execute(self, exercise_id: int, user_id: int) -> None:
        """Delete an exercise."""
        # Get existing exercise
        exercise = self.exercise_repository.get_by_id(exercise_id)
        if not exercise:
            raise ValueError(f"Exercise with id {exercise_id} not found")

        # Check ownership for custom exercises
        if exercise.is_custom and exercise.user_id != user_id:
            raise ValueError("You don't have permission to delete this exercise")

        # System exercises cannot be deleted
        if not exercise.is_custom:
            raise ValueError("System exercises cannot be deleted")

        self.exercise_repository.delete(exercise_id)



