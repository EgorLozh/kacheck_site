from typing import List
from src.domain.repositories.training_comment_repository import ITrainingCommentRepository
from src.domain.entities.training_comment import TrainingComment


class GetTrainingCommentsUseCase:
    """Use case for getting comments for a training."""

    def __init__(self, comment_repository: ITrainingCommentRepository):
        self.comment_repository = comment_repository

    def execute(self, training_id: int) -> List[TrainingComment]:
        """Get all comments for a training."""
        return self.comment_repository.get_by_training(training_id)


