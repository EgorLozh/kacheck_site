from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.training_comment import TrainingComment


class ITrainingCommentRepository(ABC):
    """Interface for Training Comment repository (Port)."""

    @abstractmethod
    def create(self, comment: TrainingComment) -> TrainingComment:
        """Create a new comment."""
        pass

    @abstractmethod
    def update(self, comment: TrainingComment) -> TrainingComment:
        """Update a comment."""
        pass

    @abstractmethod
    def delete(self, comment_id: int) -> None:
        """Delete a comment."""
        pass

    @abstractmethod
    def get_by_id(self, comment_id: int) -> Optional[TrainingComment]:
        """Get comment by ID."""
        pass

    @abstractmethod
    def get_by_training(self, training_id: int) -> List[TrainingComment]:
        """Get all comments for a training."""
        pass


