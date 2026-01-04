import secrets
from src.domain.repositories.training_repository import ITrainingRepository
from src.application.dto.training_dto import TrainingResponseDTO
from src.application.use_cases.trainings.get_training_by_id import GetTrainingByIdUseCase


class GenerateShareTokenUseCase:
    """Use case for generating or getting share token for a training."""

    def __init__(
        self,
        training_repository: ITrainingRepository,
    ):
        self.training_repository = training_repository

    def execute(self, training_id: int, user_id: int) -> TrainingResponseDTO:
        """Generate or get share token for a training."""
        # Verify training exists and belongs to user
        training = self.training_repository.get_by_id(training_id)
        if not training:
            raise ValueError(f"Training with id {training_id} not found")
        
        if training.user_id != user_id:
            raise ValueError("Training does not belong to user")

        # If token already exists, return it
        if training.share_token:
            from src.application.use_cases.trainings.get_training_by_id import GetTrainingByIdUseCase
            get_use_case = GetTrainingByIdUseCase(self.training_repository)
            return get_use_case.execute(training_id, user_id)

        # Generate new token
        share_token = secrets.token_urlsafe(32)
        training.share_token = share_token
        updated_training = self.training_repository.update(training)

        # Convert to DTO
        from src.application.use_cases.trainings.get_training_by_id import GetTrainingByIdUseCase
        get_use_case = GetTrainingByIdUseCase(self.training_repository)
        return get_use_case.execute(training_id, user_id)


