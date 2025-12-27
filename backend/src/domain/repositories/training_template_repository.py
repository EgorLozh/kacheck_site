from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.training_template import TrainingTemplate


class ITrainingTemplateRepository(ABC):
    """Interface for TrainingTemplate repository (Port)."""

    @abstractmethod
    def create(self, template: TrainingTemplate) -> TrainingTemplate:
        """Create a new training template."""
        pass

    @abstractmethod
    def get_by_id(self, template_id: int) -> Optional[TrainingTemplate]:
        """Get training template by ID."""
        pass

    @abstractmethod
    def get_all(self, user_id: Optional[int] = None, include_system: bool = True) -> List[TrainingTemplate]:
        """Get all training templates, optionally filtered by user."""
        pass

    @abstractmethod
    def update(self, template: TrainingTemplate) -> TrainingTemplate:
        """Update training template."""
        pass

    @abstractmethod
    def delete(self, template_id: int) -> None:
        """Delete training template."""
        pass

