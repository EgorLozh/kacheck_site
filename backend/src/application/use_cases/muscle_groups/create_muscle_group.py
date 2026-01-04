from datetime import datetime

from src.domain.entities.muscle_group import MuscleGroup
from src.domain.repositories.muscle_group_repository import IMuscleGroupRepository
from src.application.dto.muscle_group_dto import CreateMuscleGroupDTO, MuscleGroupResponseDTO


class CreateMuscleGroupUseCase:
    """Use case for creating a muscle group."""

    def __init__(self, muscle_group_repository: IMuscleGroupRepository):
        self.muscle_group_repository = muscle_group_repository

    def execute(self, dto: CreateMuscleGroupDTO) -> MuscleGroupResponseDTO:
        """Create a new muscle group."""
        now = datetime.utcnow()
        muscle_group = MuscleGroup(
            id=None,
            name=dto.name,
            is_system=False,  # User-created groups are not system
            created_at=now,
            updated_at=now,
        )

        created_muscle_group = self.muscle_group_repository.create(muscle_group)

        return MuscleGroupResponseDTO(
            id=created_muscle_group.id,
            name=created_muscle_group.name,
            is_system=created_muscle_group.is_system,
        )





