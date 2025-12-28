from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime

if TYPE_CHECKING:
    from .training_template import TrainingTemplate


@dataclass
class User:
    """User entity."""

    id: Optional[int]
    email: str
    username: str
    hashed_password: str
    weight: Optional[float] = None  # Current weight in kg
    height: Optional[float] = None  # Current height in cm
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_training_templates(self, templates: List["TrainingTemplate"]) -> List["TrainingTemplate"]:
        """Get training templates for this user."""
        return [template for template in templates if template.user_id == self.id]

