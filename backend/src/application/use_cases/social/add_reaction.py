from datetime import datetime
from src.domain.repositories.training_reaction_repository import ITrainingReactionRepository
from src.domain.entities.training_reaction import TrainingReaction, ReactionType


class AddReactionUseCase:
    """Use case for adding a reaction to a training."""

    def __init__(self, reaction_repository: ITrainingReactionRepository):
        self.reaction_repository = reaction_repository

    def execute(self, training_id: int, user_id: int, reaction_type: ReactionType) -> TrainingReaction:
        """Add a reaction to a training."""
        # Check if user already reacted
        existing = self.reaction_repository.get_by_training_and_user(training_id, user_id)
        if existing:
            # Update existing reaction
            existing.reaction_type = reaction_type
            # For simplicity, delete and recreate (or implement update in repository)
            self.reaction_repository.delete(existing.id)
        
        reaction = TrainingReaction(
            id=None,
            training_id=training_id,
            user_id=user_id,
            reaction_type=reaction_type,
            created_at=datetime.utcnow(),
        )

        return self.reaction_repository.create(reaction)


