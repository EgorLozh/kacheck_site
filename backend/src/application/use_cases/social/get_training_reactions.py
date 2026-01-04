from typing import List
from src.domain.repositories.training_reaction_repository import ITrainingReactionRepository
from src.domain.entities.training_reaction import TrainingReaction


class GetTrainingReactionsUseCase:
    """Use case for getting reactions for a training."""

    def __init__(self, reaction_repository: ITrainingReactionRepository):
        self.reaction_repository = reaction_repository

    def execute(self, training_id: int) -> List[TrainingReaction]:
        """Get all reactions for a training."""
        return self.reaction_repository.get_by_training(training_id)


