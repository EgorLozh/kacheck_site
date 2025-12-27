from dataclasses import dataclass
from typing import Optional


@dataclass
class SetTemplate:
    """Set template entity (template for a set in training template)."""

    id: Optional[int]
    implementation_template_id: int
    order_index: int
    weight: Optional[float]  # Optional weight value
    reps: Optional[int]  # Optional reps value

