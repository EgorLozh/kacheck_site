from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.database.base import Base


class TrainingTemplateModel(Base):
    """SQLAlchemy model for TrainingTemplate entity."""

    __tablename__ = "training_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("UserModel", back_populates="training_templates")
    implementation_templates = relationship(
        "ImplementationTemplateModel",
        back_populates="training_template",
        cascade="all, delete-orphan",
        order_by="ImplementationTemplateModel.order_index",
    )
    trainings = relationship("TrainingModel", back_populates="training_template")





