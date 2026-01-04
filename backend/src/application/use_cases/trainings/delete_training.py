from src.domain.repositories.training_repository import ITrainingRepository


class DeleteTrainingUseCase:
    """Use case for deleting a training."""

    def __init__(self, training_repository: ITrainingRepository):
        self.training_repository = training_repository

    def execute(self, training_id: int, user_id: int) -> None:
        """Delete a training."""
        # Get existing training
        training = self.training_repository.get_by_id(training_id)
        if not training:
            raise ValueError(f"Training with id {training_id} not found")

        # Check ownership
        if training.user_id != user_id:
            raise ValueError("You don't have permission to delete this training")

        self.training_repository.delete(training_id)





