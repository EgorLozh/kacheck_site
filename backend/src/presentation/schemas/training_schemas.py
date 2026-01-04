from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from src.domain.entities.training import TrainingStatus


class SetBase(BaseModel):
    """Base schema for set."""

    order_index: int
    weight: float
    reps: int
    rest_time: Optional[int] = None
    duration: Optional[int] = None
    rpe: Optional[int] = None


class ImplementationBase(BaseModel):
    """Base schema for implementation."""

    exercise_id: int
    order_index: int
    sets: List[SetBase]


class TrainingBase(BaseModel):
    """Base schema for training."""

    date_time: datetime
    duration: Optional[int] = None
    notes: Optional[str] = None
    status: TrainingStatus = TrainingStatus.PLANNED


class TrainingCreate(TrainingBase):
    """Schema for creating training."""

    training_template_id: Optional[int] = None
    implementations: Optional[List[ImplementationBase]] = None


class TrainingUpdate(BaseModel):
    """Schema for updating training."""

    date_time: Optional[datetime] = None
    implementations: Optional[List[ImplementationBase]] = None
    duration: Optional[int] = None
    notes: Optional[str] = None
    status: Optional[TrainingStatus] = None


class TrainingResponse(TrainingBase):
    """Schema for training response."""

    id: int
    user_id: int
    training_template_id: Optional[int]
    created_at: datetime
    share_token: Optional[str] = None
    username: Optional[str] = None  # Username of the training owner (for shared trainings)
    implementations: List[ImplementationBase]

    class Config:
        from_attributes = True




