from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class MuscleGroup:
    """Muscle group entity."""

    id: Optional[int]
    name: str
    is_system: bool
    created_at: datetime
    updated_at: datetime



