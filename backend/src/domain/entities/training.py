from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from enum import Enum

from .implementation import Implementation


class TrainingStatus(str, Enum):
    """Training status enum."""

    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


@dataclass
class Training:
    """Training entity (actual workout session)."""

    id: Optional[int]
    user_id: int
    training_template_id: Optional[int]  # None if created from scratch
    date_time: datetime
    duration: Optional[int]  # Duration in seconds
    notes: Optional[str]
    status: TrainingStatus
    created_at: datetime
    updated_at: datetime
    share_token: Optional[str] = None  # Token for public sharing
    implementations: List[Implementation] = field(default_factory=list)

