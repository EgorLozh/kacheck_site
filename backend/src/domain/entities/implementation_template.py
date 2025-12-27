from dataclasses import dataclass, field
from typing import Optional, List

from .set_template import SetTemplate


@dataclass
class ImplementationTemplate:
    """Implementation template entity (exercise in training template)."""

    id: Optional[int]
    training_template_id: int
    exercise_id: int
    order_index: int
    set_templates: List[SetTemplate] = field(default_factory=list)

