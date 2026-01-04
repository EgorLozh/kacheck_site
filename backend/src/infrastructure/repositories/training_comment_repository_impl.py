from typing import Optional, List
from sqlalchemy.orm import Session

from src.domain.repositories.training_comment_repository import ITrainingCommentRepository
from src.domain.entities.training_comment import TrainingComment
from src.infrastructure.database.models.training_comment_model import TrainingCommentModel


class TrainingCommentRepositoryImpl(ITrainingCommentRepository):
    """SQLAlchemy implementation of Training Comment repository (Adapter)."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, comment: TrainingComment) -> TrainingComment:
        """Create a new comment."""
        db_comment = TrainingCommentModel(
            training_id=comment.training_id,
            user_id=comment.user_id,
            text=comment.text,
        )
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return self._to_entity(db_comment)

    def update(self, comment: TrainingComment) -> TrainingComment:
        """Update a comment."""
        if comment.id is None:
            raise ValueError("Comment id is required for update")
        db_comment = (
            self.db.query(TrainingCommentModel).filter(TrainingCommentModel.id == comment.id).first()
        )
        if not db_comment:
            raise ValueError(f"Comment with id {comment.id} not found")

        db_comment.text = comment.text
        self.db.commit()
        self.db.refresh(db_comment)
        return self._to_entity(db_comment)

    def delete(self, comment_id: int) -> None:
        """Delete a comment."""
        db_comment = self.db.query(TrainingCommentModel).filter(TrainingCommentModel.id == comment_id).first()
        if db_comment:
            self.db.delete(db_comment)
            self.db.commit()

    def get_by_id(self, comment_id: int) -> Optional[TrainingComment]:
        """Get comment by ID."""
        db_comment = self.db.query(TrainingCommentModel).filter(TrainingCommentModel.id == comment_id).first()
        return self._to_entity(db_comment) if db_comment else None

    def get_by_training(self, training_id: int) -> List[TrainingComment]:
        """Get all comments for a training."""
        db_comments = (
            self.db.query(TrainingCommentModel)
            .filter(TrainingCommentModel.training_id == training_id)
            .order_by(TrainingCommentModel.created_at)
            .all()
        )
        return [self._to_entity(c) for c in db_comments]

    def _to_entity(self, db_comment: TrainingCommentModel) -> TrainingComment:
        """Convert SQLAlchemy model to domain entity."""
        return TrainingComment(
            id=db_comment.id,
            training_id=db_comment.training_id,
            user_id=db_comment.user_id,
            text=db_comment.text,
            created_at=db_comment.created_at,
            updated_at=db_comment.updated_at,
        )


