from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

from src.domain.entities.training import TrainingStatus


@dataclass
class SetDTO:
    """DTO for a set."""

    order_index: int
    weight: float
    reps: int
    rest_time: Optional[int] = None
    duration: Optional[int] = None
    rpe: Optional[int] = None


@dataclass
class ImplementationDTO:
    """DTO for an implementation (exercise in training)."""

    exercise_id: int
    order_index: int
    sets: List[SetDTO]


@dataclass
class CreateTrainingDTO:
    """DTO for creating a training."""

    date_time: datetime
    training_template_id: Optional[int] = None
    implementations: Optional[List[ImplementationDTO]] = None
    duration: Optional[int] = None
    notes: Optional[str] = None
    status: TrainingStatus = TrainingStatus.PLANNED


@dataclass
class UpdateTrainingDTO:
    """DTO for updating a training."""

    date_time: Optional[datetime] = None
    implementations: Optional[List[ImplementationDTO]] = None
    duration: Optional[int] = None
    notes: Optional[str] = None
    status: Optional[TrainingStatus] = None


@dataclass
class TrainingResponseDTO:
    """DTO for training response."""

    id: int
    user_id: int
    training_template_id: Optional[int]
    date_time: datetime
    duration: Optional[int]
    notes: Optional[str]
    status: TrainingStatus
    implementations: List[ImplementationDTO]


