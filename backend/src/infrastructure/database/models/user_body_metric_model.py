from sqlalchemy import Column, Integer, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.infrastructure.database.base import Base


class UserBodyMetricModel(Base):
    """SQLAlchemy model for User Body Metric entity (weight and height tracking)."""

    __tablename__ = "user_body_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    weight = Column(Numeric(5, 2), nullable=True)  # Weight in kg, nullable to allow only height updates
    height = Column(Numeric(5, 2), nullable=True)  # Height in cm, nullable to allow only weight updates
    date = Column(Date, nullable=False, index=True)  # Date of measurement
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("UserModel", back_populates="body_metrics")

