from typing import Optional, List

from sqlalchemy.orm import Session

from src.domain.entities.exercise import Exercise
from src.domain.repositories.exercise_repository import IExerciseRepository
from src.domain.value_objects.exercise_name import ExerciseName
from src.infrastructure.database.models.exercise_model import ExerciseModel
from src.infrastructure.database.models.exercise_muscle_group_model import ExerciseMuscleGroupModel


class ExerciseRepositoryImpl(IExerciseRepository):
    """SQLAlchemy implementation of Exercise repository (Adapter)."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, exercise: Exercise) -> Exercise:
        """Create a new exercise."""
        db_exercise = ExerciseModel(
            name=str(exercise.name),
            description=exercise.description,
            image_path=exercise.image_path,
            is_custom=exercise.is_custom,
            user_id=exercise.user_id,
        )
        self.db.add(db_exercise)
        self.db.flush()

        # Create muscle group associations
        for muscle_group_id in exercise.muscle_group_ids:
            association = ExerciseMuscleGroupModel(
                exercise_id=db_exercise.id,
                muscle_group_id=muscle_group_id,
            )
            self.db.add(association)

        self.db.commit()
        self.db.refresh(db_exercise)
        return self._to_entity(db_exercise)

    def get_by_id(self, exercise_id: int) -> Optional[Exercise]:
        """Get exercise by ID."""
        db_exercise = self.db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()
        return self._to_entity(db_exercise) if db_exercise else None

    def get_all(self, user_id: Optional[int] = None, include_system: bool = True) -> List[Exercise]:
        """Get all exercises, optionally filtered by user."""
        query = self.db.query(ExerciseModel)

        if not include_system:
            query = query.filter(ExerciseModel.is_custom == True)  # noqa: E712

        if user_id is not None:
            query = query.filter(
                (ExerciseModel.user_id == user_id) | (ExerciseModel.is_custom == False)  # noqa: E712
            )

        db_exercises = query.all()
        return [self._to_entity(ex) for ex in db_exercises]

    def update(self, exercise: Exercise) -> Exercise:
        """Update exercise."""
        if exercise.id is None:
            raise ValueError("Exercise id is required for update")
        db_exercise = self.db.query(ExerciseModel).filter(ExerciseModel.id == exercise.id).first()
        if not db_exercise:
            raise ValueError(f"Exercise with id {exercise.id} not found")

        db_exercise.name = str(exercise.name)
        db_exercise.description = exercise.description
        db_exercise.image_path = exercise.image_path
        db_exercise.is_custom = exercise.is_custom

        # Update muscle group associations
        self.db.query(ExerciseMuscleGroupModel).filter(
            ExerciseMuscleGroupModel.exercise_id == exercise.id
        ).delete()
        for muscle_group_id in exercise.muscle_group_ids:
            association = ExerciseMuscleGroupModel(
                exercise_id=db_exercise.id,
                muscle_group_id=muscle_group_id,
            )
            self.db.add(association)

        self.db.commit()
        self.db.refresh(db_exercise)
        return self._to_entity(db_exercise)

    def delete(self, exercise_id: int) -> None:
        """Delete exercise."""
        db_exercise = self.db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()
        if db_exercise:
            self.db.delete(db_exercise)
            self.db.commit()

    def get_by_muscle_group(self, muscle_group_id: int) -> List[Exercise]:
        """Get exercises by muscle group."""
        db_associations = (
            self.db.query(ExerciseMuscleGroupModel)
            .filter(ExerciseMuscleGroupModel.muscle_group_id == muscle_group_id)
            .all()
        )
        exercise_ids = [assoc.exercise_id for assoc in db_associations]
        db_exercises = self.db.query(ExerciseModel).filter(ExerciseModel.id.in_(exercise_ids)).all()
        return [self._to_entity(ex) for ex in db_exercises]

    def _to_entity(self, db_exercise: ExerciseModel) -> Exercise:
        """Convert SQLAlchemy model to domain entity."""
        # Get muscle group IDs
        associations = (
            self.db.query(ExerciseMuscleGroupModel)
            .filter(ExerciseMuscleGroupModel.exercise_id == db_exercise.id)
            .all()
        )
        muscle_group_ids = [assoc.muscle_group_id for assoc in associations]

        return Exercise(
            id=db_exercise.id,
            name=ExerciseName(db_exercise.name),
            description=db_exercise.description,
            image_path=db_exercise.image_path,
            is_custom=db_exercise.is_custom,
            user_id=db_exercise.user_id,
            muscle_group_ids=muscle_group_ids,
            created_at=db_exercise.created_at,
            updated_at=db_exercise.updated_at,
        )

