from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from src.infrastructure.database.base import Base


class SetTemplateModel(Base):
    """SQLAlchemy model for SetTemplate entity."""

    __tablename__ = "set_templates"

    id = Column(Integer, primary_key=True, index=True)
    implementation_template_id = Column(
        Integer, ForeignKey("implementation_templates.id", ondelete="CASCADE"), nullable=False
    )
    order_index = Column(Integer, nullable=False)
    weight = Column(Numeric(10, 2), nullable=True)
    reps = Column(Integer, nullable=True)

    # Relationships
    implementation_template = relationship("ImplementationTemplateModel", back_populates="set_templates")

