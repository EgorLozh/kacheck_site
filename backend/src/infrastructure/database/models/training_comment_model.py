from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.database.base import Base


class TrainingCommentModel(Base):
    """SQLAlchemy model for Training Comment entity."""

    __tablename__ = "training_comments"

    id = Column(Integer, primary_key=True, index=True)
    training_id = Column(Integer, ForeignKey("trainings.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    training = relationship("TrainingModel", back_populates="comments")
    user = relationship("UserModel", back_populates="training_comments")


