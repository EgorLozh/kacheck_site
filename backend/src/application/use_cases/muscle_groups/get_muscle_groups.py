from typing import List

from src.domain.repositories.muscle_group_repository import IMuscleGroupRepository
from src.application.dto.muscle_group_dto import MuscleGroupResponseDTO


class GetMuscleGroupsUseCase:
    """Use case for getting muscle groups."""

    def __init__(self, muscle_group_repository: IMuscleGroupRepository):
        self.muscle_group_repository = muscle_group_repository

    def execute(self, include_system: bool = True) -> List[MuscleGroupResponseDTO]:
        """Get all muscle groups."""
        muscle_groups = self.muscle_group_repository.get_all(include_system=include_system)

        return [
            MuscleGroupResponseDTO(
                id=mg.id,
                name=mg.name,
                is_system=mg.is_system,
            )
            for mg in muscle_groups
        ]


