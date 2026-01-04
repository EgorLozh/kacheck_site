from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.infrastructure.database.base import Base


class ImplementationTemplateModel(Base):
    """SQLAlchemy model for ImplementationTemplate entity."""

    __tablename__ = "implementation_templates"

    id = Column(Integer, primary_key=True, index=True)
    training_template_id = Column(Integer, ForeignKey("training_templates.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    order_index = Column(Integer, nullable=False)

    # Relationships
    training_template = relationship("TrainingTemplateModel", back_populates="implementation_templates")
    exercise = relationship("ExerciseModel", back_populates="implementation_templates")
    set_templates = relationship(
        "SetTemplateModel",
        back_populates="implementation_template",
        cascade="all, delete-orphan",
        order_by="SetTemplateModel.order_index",
    )





