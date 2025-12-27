from dataclasses import dataclass, field
from typing import Optional, List

from .set import Set


@dataclass
class Implementation:
    """Implementation entity (exercise execution in training)."""

    id: Optional[int]
    training_id: int
    exercise_id: int
    order_index: int
    sets: List[Set] = field(default_factory=list)

