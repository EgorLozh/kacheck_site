from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.database.base import Base


class TrainingReactionModel(Base):
    """SQLAlchemy model for Training Reaction entity."""

    __tablename__ = "training_reactions"

    id = Column(Integer, primary_key=True, index=True)
    training_id = Column(Integer, ForeignKey("trainings.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reaction_type = Column(String, nullable=False)  # LIKE, LOVE, FIRE, MUSCLE, TARGET
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    training = relationship("TrainingModel", back_populates="reactions")
    user = relationship("UserModel", back_populates="training_reactions")

    # Unique constraint: user cannot react to the same training twice
    __table_args__ = (
        UniqueConstraint('training_id', 'user_id', name='uq_training_reaction'),
    )


