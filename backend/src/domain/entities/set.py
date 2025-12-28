from dataclasses import dataclass
from typing import Optional

from ..value_objects.weight import Weight
from ..value_objects.reps import Reps
from ..value_objects.rest_time import RestTime
from ..value_objects.duration import Duration
from ..value_objects.rpe import RPE


@dataclass
class Set:
    """Set entity (actual set execution in training)."""

    id: Optional[int]
    implementation_id: int
    order_index: int
    weight: Weight
    reps: Reps
    rest_time: Optional[RestTime]
    duration: Optional[Duration]
    rpe: Optional[RPE]


