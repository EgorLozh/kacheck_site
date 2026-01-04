from typing import Optional, List
from sqlalchemy.orm import Session

from src.domain.repositories.training_reaction_repository import ITrainingReactionRepository
from src.domain.entities.training_reaction import TrainingReaction, ReactionType
from src.infrastructure.database.models.training_reaction_model import TrainingReactionModel


class TrainingReactionRepositoryImpl(ITrainingReactionRepository):
    """SQLAlchemy implementation of Training Reaction repository (Adapter)."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, reaction: TrainingReaction) -> TrainingReaction:
        """Create a new reaction."""
        db_reaction = TrainingReactionModel(
            training_id=reaction.training_id,
            user_id=reaction.user_id,
            reaction_type=reaction.reaction_type.value,
        )
        self.db.add(db_reaction)
        self.db.commit()
        self.db.refresh(db_reaction)
        return self._to_entity(db_reaction)

    def delete(self, reaction_id: int) -> None:
        """Delete a reaction."""
        db_reaction = self.db.query(TrainingReactionModel).filter(TrainingReactionModel.id == reaction_id).first()
        if db_reaction:
            self.db.delete(db_reaction)
            self.db.commit()

    def get_by_training_and_user(self, training_id: int, user_id: int) -> Optional[TrainingReaction]:
        """Get reaction by training and user IDs."""
        db_reaction = (
            self.db.query(TrainingReactionModel)
            .filter(
                TrainingReactionModel.training_id == training_id,
                TrainingReactionModel.user_id == user_id,
            )
            .first()
        )
        return self._to_entity(db_reaction) if db_reaction else None

    def get_by_training(self, training_id: int) -> List[TrainingReaction]:
        """Get all reactions for a training."""
        db_reactions = (
            self.db.query(TrainingReactionModel)
            .filter(TrainingReactionModel.training_id == training_id)
            .all()
        )
        return [self._to_entity(r) for r in db_reactions]

    def _to_entity(self, db_reaction: TrainingReactionModel) -> TrainingReaction:
        """Convert SQLAlchemy model to domain entity."""
        return TrainingReaction(
            id=db_reaction.id,
            training_id=db_reaction.training_id,
            user_id=db_reaction.user_id,
            reaction_type=ReactionType(db_reaction.reaction_type),
            created_at=db_reaction.created_at,
        )


