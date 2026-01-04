from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.training_reaction import TrainingReaction


class ITrainingReactionRepository(ABC):
    """Interface for Training Reaction repository (Port)."""

    @abstractmethod
    def create(self, reaction: TrainingReaction) -> TrainingReaction:
        """Create a new reaction."""
        pass

    @abstractmethod
    def delete(self, reaction_id: int) -> None:
        """Delete a reaction."""
        pass

    @abstractmethod
    def get_by_training_and_user(self, training_id: int, user_id: int) -> Optional[TrainingReaction]:
        """Get reaction by training and user IDs."""
        pass

    @abstractmethod
    def get_by_training(self, training_id: int) -> List[TrainingReaction]:
        """Get all reactions for a training."""
        pass


