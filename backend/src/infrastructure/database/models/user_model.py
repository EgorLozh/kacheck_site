from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.database.base import Base


class UserModel(Base):
    """SQLAlchemy model for User entity."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    weight = Column(Numeric(5, 2), nullable=True)  # Current weight in kg
    height = Column(Numeric(5, 2), nullable=True)  # Current height in cm
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    training_templates = relationship("TrainingTemplateModel", back_populates="user", cascade="all, delete-orphan")
    exercises = relationship("ExerciseModel", back_populates="user", cascade="all, delete-orphan")
    trainings = relationship("TrainingModel", back_populates="user", cascade="all, delete-orphan")
    body_metrics = relationship("UserBodyMetricModel", back_populates="user", cascade="all, delete-orphan")
    following = relationship("FollowModel", foreign_keys="FollowModel.follower_id", back_populates="follower", cascade="all, delete-orphan")
    followers = relationship("FollowModel", foreign_keys="FollowModel.following_id", back_populates="following_user", cascade="all, delete-orphan")
    training_reactions = relationship("TrainingReactionModel", back_populates="user", cascade="all, delete-orphan")
    training_comments = relationship("TrainingCommentModel", back_populates="user", cascade="all, delete-orphan")


