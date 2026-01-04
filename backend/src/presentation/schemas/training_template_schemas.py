from pydantic import BaseModel
from typing import Optional, List


class SetTemplateBase(BaseModel):
    """Base schema for set template."""

    order_index: int
    weight: Optional[float] = None
    reps: Optional[int] = None


class ImplementationTemplateBase(BaseModel):
    """Base schema for implementation template."""

    exercise_id: int
    order_index: int
    set_templates: List[SetTemplateBase]


class TemplateBase(BaseModel):
    """Base schema for training template."""

    name: str
    description: Optional[str] = None


class TemplateCreate(TemplateBase):
    """Schema for creating training template."""

    implementation_templates: List[ImplementationTemplateBase]


class TemplateUpdate(BaseModel):
    """Schema for updating training template."""

    name: Optional[str] = None
    description: Optional[str] = None
    implementation_templates: Optional[List[ImplementationTemplateBase]] = None


class TemplateResponse(TemplateBase):
    """Schema for training template response."""

    id: int
    user_id: Optional[int]
    implementation_templates: List[ImplementationTemplateBase]

    class Config:
        from_attributes = True





