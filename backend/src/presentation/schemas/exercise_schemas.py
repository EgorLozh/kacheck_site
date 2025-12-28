from pydantic import BaseModel
from typing import Optional, List


class ExerciseBase(BaseModel):
    """Base schema for exercise."""

    name: str
    description: Optional[str] = None
    muscle_group_ids: List[int]


class ExerciseCreate(ExerciseBase):
    """Schema for creating exercise."""

    image_path: Optional[str] = None


class ExerciseUpdate(BaseModel):
    """Schema for updating exercise."""

    name: Optional[str] = None
    description: Optional[str] = None
    muscle_group_ids: Optional[List[int]] = None
    image_path: Optional[str] = None


class ExerciseResponse(ExerciseBase):
    """Schema for exercise response."""

    id: int
    image_path: Optional[str]
    is_custom: bool
    user_id: Optional[int]

    class Config:
        from_attributes = True



