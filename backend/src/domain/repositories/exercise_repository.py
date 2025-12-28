from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.exercise import Exercise


class IExerciseRepository(ABC):
    """Interface for Exercise repository (Port)."""

    @abstractmethod
    def create(self, exercise: Exercise) -> Exercise:
        """Create a new exercise."""
        pass

    @abstractmethod
    def get_by_id(self, exercise_id: int) -> Optional[Exercise]:
        """Get exercise by ID."""
        pass

    @abstractmethod
    def get_all(self, user_id: Optional[int] = None, include_system: bool = True) -> List[Exercise]:
        """Get all exercises, optionally filtered by user."""
        pass

    @abstractmethod
    def update(self, exercise: Exercise) -> Exercise:
        """Update exercise."""
        pass

    @abstractmethod
    def delete(self, exercise_id: int) -> None:
        """Delete exercise."""
        pass

    @abstractmethod
    def get_by_muscle_group(self, muscle_group_id: int) -> List[Exercise]:
        """Get exercises by muscle group."""
        pass


