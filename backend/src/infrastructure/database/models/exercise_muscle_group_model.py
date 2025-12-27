from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.infrastructure.database.base import Base


class ExerciseMuscleGroupModel(Base):
    """Association model for Exercise-MuscleGroup many-to-many relationship."""

    __tablename__ = "exercise_muscle_groups"

    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), primary_key=True)
    muscle_group_id = Column(Integer, ForeignKey("muscle_groups.id", ondelete="CASCADE"), primary_key=True)

    # Relationships
    exercise = relationship("ExerciseModel", back_populates="muscle_group_associations")
    muscle_group = relationship("MuscleGroupModel", back_populates="exercises")

