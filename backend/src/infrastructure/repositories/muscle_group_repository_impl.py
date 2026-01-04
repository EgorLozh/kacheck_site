from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import Session

from src.domain.entities.muscle_group import MuscleGroup
from src.domain.repositories.muscle_group_repository import IMuscleGroupRepository
from src.infrastructure.database.models.muscle_group_model import MuscleGroupModel


class MuscleGroupRepositoryImpl(IMuscleGroupRepository):
    """SQLAlchemy implementation of MuscleGroup repository (Adapter)."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, muscle_group: MuscleGroup) -> MuscleGroup:
        """Create a new muscle group."""
        db_muscle_group = MuscleGroupModel(
            name=muscle_group.name,
            is_system=muscle_group.is_system,
            created_at=muscle_group.created_at,
            updated_at=muscle_group.updated_at,
        )
        self.db.add(db_muscle_group)
        self.db.commit()
        self.db.refresh(db_muscle_group)
        return self._to_entity(db_muscle_group)

    def get_by_id(self, muscle_group_id: int) -> Optional[MuscleGroup]:
        """Get muscle group by ID."""
        db_muscle_group = (
            self.db.query(MuscleGroupModel).filter(MuscleGroupModel.id == muscle_group_id).first()
        )
        return self._to_entity(db_muscle_group) if db_muscle_group else None

    def get_all(self, include_system: bool = True) -> List[MuscleGroup]:
        """Get all muscle groups."""
        query = self.db.query(MuscleGroupModel)
        if not include_system:
            query = query.filter(MuscleGroupModel.is_system == False)  # noqa: E712
        db_muscle_groups = query.all()
        return [self._to_entity(mg) for mg in db_muscle_groups]

    def update(self, muscle_group: MuscleGroup) -> MuscleGroup:
        """Update muscle group."""
        if muscle_group.id is None:
            raise ValueError("Muscle group id is required for update")
        db_muscle_group = (
            self.db.query(MuscleGroupModel).filter(MuscleGroupModel.id == muscle_group.id).first()
        )
        if not db_muscle_group:
            raise ValueError(f"Muscle group with id {muscle_group.id} not found")

        db_muscle_group.name = muscle_group.name
        db_muscle_group.is_system = muscle_group.is_system
        db_muscle_group.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(db_muscle_group)
        return self._to_entity(db_muscle_group)

    def delete(self, muscle_group_id: int) -> None:
        """Delete muscle group."""
        db_muscle_group = (
            self.db.query(MuscleGroupModel).filter(MuscleGroupModel.id == muscle_group_id).first()
        )
        if db_muscle_group:
            self.db.delete(db_muscle_group)
            self.db.commit()

    @staticmethod
    def _to_entity(db_muscle_group: MuscleGroupModel) -> MuscleGroup:
        """Convert SQLAlchemy model to domain entity."""
        return MuscleGroup(
            id=db_muscle_group.id,
            name=db_muscle_group.name,
            is_system=db_muscle_group.is_system,
            created_at=db_muscle_group.created_at,
            updated_at=db_muscle_group.updated_at,
        )





