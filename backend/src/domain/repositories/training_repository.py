from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime

from ..entities.training import Training


class ITrainingRepository(ABC):
    """Interface for Training repository (Port)."""

    @abstractmethod
    def create(self, training: Training) -> Training:
        """Create a new training."""
        pass

    @abstractmethod
    def get_by_id(self, training_id: int) -> Optional[Training]:
        """Get training by ID."""
        pass

    @abstractmethod
    def get_all(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Training]:
        """Get all trainings for a user, optionally filtered by date range."""
        pass

    @abstractmethod
    def update(self, training: Training) -> Training:
        """Update training."""
        pass

    @abstractmethod
    def delete(self, training_id: int) -> None:
        """Delete training."""
        pass

