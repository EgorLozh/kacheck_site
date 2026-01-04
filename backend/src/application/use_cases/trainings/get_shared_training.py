from src.domain.repositories.training_repository import ITrainingRepository
from src.application.dto.training_dto import TrainingResponseDTO
from src.application.use_cases.trainings.get_training_by_id import GetTrainingByIdUseCase


class GetSharedTrainingUseCase:
    """Use case for getting a shared training by token (no authentication required)."""

    def __init__(
        self,
        training_repository: ITrainingRepository,
    ):
        self.training_repository = training_repository

    def execute(self, share_token: str) -> TrainingResponseDTO:
        """Get shared training by token."""
        training = self.training_repository.get_by_share_token(share_token)
        if not training:
            raise ValueError(f"Training with share token {share_token} not found")

        # Convert to DTO (same as GetTrainingByIdUseCase)
        from src.application.use_cases.trainings.get_training_by_id import GetTrainingByIdUseCase
        get_use_case = GetTrainingByIdUseCase(self.training_repository)
        # We need to convert manually since we don't have user_id
        from src.application.dto.training_dto import ImplementationDTO, SetDTO
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
            created_at=training.created_at,
            share_token=training.share_token,
            implementations=impl_dtos,
        )

