from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

from .implementation_template import ImplementationTemplate


@dataclass
class TrainingTemplate:
    """Training template entity."""

    id: Optional[int]
    name: str
    description: Optional[str]
    user_id: Optional[int]  # None for system templates
    created_at: datetime
    updated_at: datetime
    implementation_templates: List[ImplementationTemplate] = field(default_factory=list)

