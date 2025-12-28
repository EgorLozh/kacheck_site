from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from src.domain.entities.training import Training, TrainingStatus
from src.domain.entities.implementation import Implementation
from src.domain.entities.set import Set
from src.domain.value_objects.weight import Weight
from src.domain.value_objects.reps import Reps
from src.domain.value_objects.rest_time import RestTime
from src.domain.value_objects.duration import Duration
from src.domain.value_objects.rpe import RPE
from src.domain.repositories.training_repository import ITrainingRepository
from src.infrastructure.database.models.training_model import TrainingModel
from src.infrastructure.database.models.implementation_model import ImplementationModel
from src.infrastructure.database.models.set_model import SetModel


class TrainingRepositoryImpl(ITrainingRepository):
    """SQLAlchemy implementation of Training repository (Adapter)."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, training: Training) -> Training:
        """Create a new training."""
        db_training = TrainingModel(
            user_id=training.user_id,
            training_template_id=training.training_template_id,
            date_time=training.date_time,
            duration=training.duration,
            notes=training.notes,
            status=training.status,
        )
        self.db.add(db_training)
        self.db.flush()

        # Create implementations
        for impl in training.implementations:
            db_impl = ImplementationModel(
                training_id=db_training.id,
                exercise_id=impl.exercise_id,
                order_index=impl.order_index,
            )
            self.db.add(db_impl)
            self.db.flush()

            # Create sets
            for set_entity in impl.sets:
                db_set = SetModel(
                    implementation_id=db_impl.id,
                    order_index=set_entity.order_index,
                    weight=float(set_entity.weight.value),
                    reps=int(set_entity.reps.value),
                    rest_time=int(set_entity.rest_time.value) if set_entity.rest_time else None,
                    duration=int(set_entity.duration.value) if set_entity.duration else None,
                    rpe=int(set_entity.rpe.value) if set_entity.rpe else None,
                )
                self.db.add(db_set)

        self.db.commit()
        self.db.refresh(db_training)
        return self._to_entity(db_training)

    def get_by_id(self, training_id: int) -> Optional[Training]:
        """Get training by ID."""
        db_training = (
            self.db.query(TrainingModel)
            .options(
                joinedload(TrainingModel.implementations).joinedload(ImplementationModel.sets)
            )
            .filter(TrainingModel.id == training_id)
            .first()
        )
        return self._to_entity(db_training) if db_training else None

    def get_all(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Training]:
        """Get all trainings for a user, optionally filtered by date range."""
        query = (
            self.db.query(TrainingModel)
            .options(joinedload(TrainingModel.implementations).joinedload(ImplementationModel.sets))
            .filter(TrainingModel.user_id == user_id)
        )

        if start_date:
            query = query.filter(TrainingModel.date_time >= start_date)
        if end_date:
            query = query.filter(TrainingModel.date_time <= end_date)

        query = query.order_by(TrainingModel.date_time.desc())

        db_trainings = query.all()
        return [self._to_entity(t) for t in db_trainings]

    def update(self, training: Training) -> Training:
        """Update training."""
        if training.id is None:
            raise ValueError("Training id is required for update")
        db_training = (
            self.db.query(TrainingModel).filter(TrainingModel.id == training.id).first()
        )
        if not db_training:
            raise ValueError(f"Training with id {training.id} not found")

        db_training.date_time = training.date_time
        db_training.duration = training.duration
        db_training.notes = training.notes
        db_training.status = training.status

        # Delete old implementations
        self.db.query(ImplementationModel).filter(
            ImplementationModel.training_id == training.id
        ).delete()

        # Create new implementations
        for impl in training.implementations:
            db_impl = ImplementationModel(
                training_id=db_training.id,
                exercise_id=impl.exercise_id,
                order_index=impl.order_index,
            )
            self.db.add(db_impl)
            self.db.flush()

            for set_entity in impl.sets:
                db_set = SetModel(
                    implementation_id=db_impl.id,
                    order_index=set_entity.order_index,
                    weight=float(set_entity.weight.value),
                    reps=int(set_entity.reps.value),
                    rest_time=int(set_entity.rest_time.value) if set_entity.rest_time else None,
                    duration=int(set_entity.duration.value) if set_entity.duration else None,
                    rpe=int(set_entity.rpe.value) if set_entity.rpe else None,
                )
                self.db.add(db_set)

        self.db.commit()
        self.db.refresh(db_training)
        return self._to_entity(db_training)

    def delete(self, training_id: int) -> None:
        """Delete training."""
        db_training = (
            self.db.query(TrainingModel).filter(TrainingModel.id == training_id).first()
        )
        if db_training:
            self.db.delete(db_training)
            self.db.commit()

    def _to_entity(self, db_training: TrainingModel) -> Training:
        """Convert SQLAlchemy model to domain entity."""
        implementations = []
        for db_impl in db_training.implementations:
            sets = []
            for db_set in db_impl.sets:
                sets.append(
                    Set(
                        id=db_set.id,
                        implementation_id=db_set.implementation_id,
                        order_index=db_set.order_index,
                        weight=Weight(float(db_set.weight)),
                        reps=Reps(int(db_set.reps)),
                        rest_time=RestTime.optional(db_set.rest_time),
                        duration=Duration.optional(db_set.duration),
                        rpe=RPE.optional(db_set.rpe),
                    )
                )
            implementations.append(
                Implementation(
                    id=db_impl.id,
                    training_id=db_impl.training_id,
                    exercise_id=db_impl.exercise_id,
                    order_index=db_impl.order_index,
                    sets=sets,
                )
            )

        return Training(
            id=db_training.id,
            user_id=db_training.user_id,
            training_template_id=db_training.training_template_id,
            date_time=db_training.date_time,
            duration=db_training.duration,
            notes=db_training.notes,
            status=TrainingStatus(db_training.status.value),
            implementations=implementations,
            created_at=db_training.created_at,
            updated_at=db_training.updated_at,
        )


