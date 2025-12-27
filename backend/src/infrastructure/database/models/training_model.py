from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.database.base import Base
from src.domain.entities.training import TrainingStatus


class TrainingModel(Base):
    """SQLAlchemy model for Training entity."""

    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    training_template_id = Column(Integer, ForeignKey("training_templates.id", ondelete="SET NULL"), nullable=True)
    date_time = Column(DateTime(timezone=True), nullable=False)
    duration = Column(Integer, nullable=True)  # Duration in seconds
    notes = Column(String, nullable=True)
    status = Column(SQLEnum(TrainingStatus), nullable=False, default=TrainingStatus.PLANNED)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("UserModel", back_populates="trainings")
    training_template = relationship("TrainingTemplateModel", back_populates="trainings")
    implementations = relationship(
        "ImplementationModel",
        back_populates="training",
        cascade="all, delete-orphan",
        order_by="ImplementationModel.order_index",
    )

