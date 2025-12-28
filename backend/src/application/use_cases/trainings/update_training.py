from src.domain.entities.training import Training, TrainingStatus
from src.domain.entities.implementation import Implementation
from src.domain.entities.set import Set
from src.domain.value_objects.weight import Weight
from src.domain.value_objects.reps import Reps
from src.domain.value_objects.rest_time import RestTime
from src.domain.value_objects.duration import Duration
from src.domain.value_objects.rpe import RPE
from src.domain.repositories.training_repository import ITrainingRepository
from src.application.dto.training_dto import UpdateTrainingDTO, TrainingResponseDTO, ImplementationDTO, SetDTO


class UpdateTrainingUseCase:
    """Use case for updating a training."""

    def __init__(self, training_repository: ITrainingRepository):
        self.training_repository = training_repository

    def execute(self, training_id: int, dto: UpdateTrainingDTO, user_id: int) -> TrainingResponseDTO:
        """Update a training."""
        # Get existing training
        training = self.training_repository.get_by_id(training_id)
        if not training:
            raise ValueError(f"Training with id {training_id} not found")

        # Check ownership
        if training.user_id != user_id:
            raise ValueError("You don't have permission to update this training")

        # Update fields
        if dto.date_time is not None:
            training.date_time = dto.date_time
        if dto.duration is not None:
            training.duration = dto.duration
        if dto.notes is not None:
            training.notes = dto.notes
        if dto.status is not None:
            training.status = dto.status
        if dto.implementations is not None:
            # Convert DTOs to domain entities
            implementations = []
            for impl_dto in dto.implementations:
                sets = []
                for set_dto in impl_dto.sets:
                    sets.append(
                        Set(
                            id=None,
                            implementation_id=0,
                            order_index=set_dto.order_index,
                            weight=Weight(set_dto.weight),
                            reps=Reps(set_dto.reps),
                            rest_time=RestTime.optional(set_dto.rest_time),
                            duration=Duration.optional(set_dto.duration),
                            rpe=RPE.optional(set_dto.rpe),
                        )
                    )
                implementations.append(
                    Implementation(
                        id=None,
                        training_id=training.id,
                        exercise_id=impl_dto.exercise_id,
                        order_index=impl_dto.order_index,
                        sets=sets,
                    )
                )
            training.implementations = implementations

        updated_training = self.training_repository.update(training)
        return self._to_dto(updated_training)

    @staticmethod
    def _to_dto(training: Training) -> TrainingResponseDTO:
        """Convert domain entity to DTO."""
        impl_dtos = []
        for impl in training.implementations:
            set_dtos = [
                SetDTO(
                    order_index=s.order_index,
                    weight=float(s.weight.value),
                    reps=int(s.reps.value),
                    rest_time=int(s.rest_time.value) if s.rest_time else None,
                    duration=int(s.duration.value) if s.duration else None,
                    rpe=int(s.rpe.value) if s.rpe else None,
                )
                for s in impl.sets
            ]
            impl_dtos.append(
                ImplementationDTO(
                    exercise_id=impl.exercise_id,
                    order_index=impl.order_index,
                    sets=set_dtos,
                )
            )

        return TrainingResponseDTO(
            id=training.id,
            user_id=training.user_id,
            training_template_id=training.training_template_id,
            date_time=training.date_time,
            duration=training.duration,
            notes=training.notes,
            status=training.status,
            implementations=impl_dtos,
        )



