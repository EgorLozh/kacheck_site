from src.domain.repositories.training_reaction_repository import ITrainingReactionRepository


class RemoveReactionUseCase:
    """Use case for removing a reaction from a training."""

    def __init__(self, reaction_repository: ITrainingReactionRepository):
        self.reaction_repository = reaction_repository

    def execute(self, training_id: int, user_id: int) -> None:
        """Remove a reaction from a training."""
        reaction = self.reaction_repository.get_by_training_and_user(training_id, user_id)
        if not reaction:
            raise ValueError("Reaction not found")

        self.reaction_repository.delete(reaction.id)


