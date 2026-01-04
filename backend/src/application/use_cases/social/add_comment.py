from datetime import datetime
from src.domain.repositories.training_comment_repository import ITrainingCommentRepository
from src.domain.entities.training_comment import TrainingComment


class AddCommentUseCase:
    """Use case for adding a comment to a training."""

    def __init__(self, comment_repository: ITrainingCommentRepository):
        self.comment_repository = comment_repository

    def execute(self, training_id: int, user_id: int, text: str) -> TrainingComment:
        """Add a comment to a training."""
        if not text or not text.strip():
            raise ValueError("Comment text cannot be empty")

        now = datetime.utcnow()
        comment = TrainingComment(
            id=None,
            training_id=training_id,
            user_id=user_id,
            text=text.strip(),
            created_at=now,
            updated_at=now,
        )

        return self.comment_repository.create(comment)


