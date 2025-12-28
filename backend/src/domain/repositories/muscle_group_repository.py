from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.muscle_group import MuscleGroup


class IMuscleGroupRepository(ABC):
    """Interface for MuscleGroup repository (Port)."""

    @abstractmethod
    def create(self, muscle_group: MuscleGroup) -> MuscleGroup:
        """Create a new muscle group."""
        pass

    @abstractmethod
    def get_by_id(self, muscle_group_id: int) -> Optional[MuscleGroup]:
        """Get muscle group by ID."""
        pass

    @abstractmethod
    def get_all(self, include_system: bool = True) -> List[MuscleGroup]:
        """Get all muscle groups."""
        pass

    @abstractmethod
    def update(self, muscle_group: MuscleGroup) -> MuscleGroup:
        """Update muscle group."""
        pass

    @abstractmethod
    def delete(self, muscle_group_id: int) -> None:
        """Delete muscle group."""
        pass



