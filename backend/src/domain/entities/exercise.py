from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

from ..value_objects.exercise_name import ExerciseName


@dataclass
class Exercise:
    """Exercise entity."""

    id: Optional[int]
    name: ExerciseName
    description: Optional[str]
    image_path: Optional[str]
    is_custom: bool
    user_id: Optional[int]  # None for system exercises
    muscle_group_ids: List[int]  # Many-to-many relationship
    created_at: datetime
    updated_at: datetime

