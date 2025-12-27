from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.infrastructure.database.base import Base


class ImplementationModel(Base):
    """SQLAlchemy model for Implementation entity."""

    __tablename__ = "implementations"

    id = Column(Integer, primary_key=True, index=True)
    training_id = Column(Integer, ForeignKey("trainings.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    order_index = Column(Integer, nullable=False)

    # Relationships
    training = relationship("TrainingModel", back_populates="implementations")
    exercise = relationship("ExerciseModel", back_populates="implementations")
    sets = relationship(
        "SetModel",
        back_populates="implementation",
        cascade="all, delete-orphan",
        order_by="SetModel.order_index",
    )

