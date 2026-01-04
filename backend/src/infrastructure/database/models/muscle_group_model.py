from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.database.base import Base


class MuscleGroupModel(Base):
    """SQLAlchemy model for MuscleGroup entity."""

    __tablename__ = "muscle_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_system = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    exercises = relationship(
        "ExerciseMuscleGroupModel",
        back_populates="muscle_group",
        cascade="all, delete-orphan",
    )





