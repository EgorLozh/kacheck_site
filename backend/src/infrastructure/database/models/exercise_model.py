from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.database.base import Base


class ExerciseModel(Base):
    """SQLAlchemy model for Exercise entity."""

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image_path = Column(String, nullable=True)
    is_custom = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("UserModel", back_populates="exercises")
    muscle_group_associations = relationship(
        "ExerciseMuscleGroupModel",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )
    implementation_templates = relationship(
        "ImplementationTemplateModel",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )
    implementations = relationship(
        "ImplementationModel",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )





