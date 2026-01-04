from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from src.infrastructure.database.base import Base


class SetModel(Base):
    """SQLAlchemy model for Set entity."""

    __tablename__ = "sets"

    id = Column(Integer, primary_key=True, index=True)
    implementation_id = Column(Integer, ForeignKey("implementations.id", ondelete="CASCADE"), nullable=False)
    order_index = Column(Integer, nullable=False)
    weight = Column(Numeric(10, 2), nullable=False)
    reps = Column(Integer, nullable=False)
    rest_time = Column(Integer, nullable=True)  # Rest time in seconds
    duration = Column(Integer, nullable=True)  # Duration in seconds
    rpe = Column(Integer, nullable=True)  # RPE 1-10

    # Relationships
    implementation = relationship("ImplementationModel", back_populates="sets")





