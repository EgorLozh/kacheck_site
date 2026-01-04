from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class TrainingComment:
    """Training comment entity."""

    id: Optional[int]
    training_id: int
    user_id: int
    text: str
    created_at: datetime
    updated_at: datetime


