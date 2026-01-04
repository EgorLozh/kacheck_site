from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.database.base import Base
from src.domain.entities.follow import FollowStatus


class FollowModel(Base):
    """SQLAlchemy model for Follow entity (user follows another user)."""

    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    following_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(SQLEnum(FollowStatus, native_enum=True), nullable=False, default=FollowStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    follower = relationship("UserModel", foreign_keys=[follower_id], back_populates="following")
    following_user = relationship("UserModel", foreign_keys=[following_id], back_populates="followers")

    # Unique constraint: user cannot follow the same user twice
    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='uq_follower_following'),
    )


