from typing import List
from datetime import datetime
from src.domain.repositories.training_repository import ITrainingRepository
from src.domain.repositories.follow_repository import IFollowRepository
from src.domain.entities.follow import FollowStatus
from src.application.dto.training_dto import TrainingResponseDTO, ImplementationDTO, SetDTO


class GetUserTrainingsUseCase:
    """Use case for getting another user's trainings (requires approved follow)."""

    def __init__(
        self,
        training_repository: ITrainingRepository,
        follow_repository: IFollowRepository,
    ):
        self.training_repository = training_repository
        self.follow_repository = follow_repository

    def execute(
        self,
        user_id: int,
        current_user_id: int,
        start_date: datetime = None,
        end_date: datetime = None,
    ) -> List[TrainingResponseDTO]:
        """Get user trainings. Requires approved follow relationship."""
        # Check if viewing own trainings
        if user_id == current_user_id:
            trainings = self.training_repository.get_all(user_id, start_date, end_date)
            return [self._to_dto(t) for t in trainings]
        
        # Check if current user has approved follow relationship with the requested user
        follow = self.follow_repository.get_by_ids(current_user_id, user_id)
        if not follow or follow.status != FollowStatus.APPROVED:
            raise ValueError("Access denied: You must be an approved follower to view this user's trainings")
        
        # Get trainings
        trainings = self.training_repository.get_all(user_id, start_date, end_date)
        return [self._to_dto(t) for t in trainings]

    @staticmethod
    def _to_dto(training) -> TrainingResponseDTO:
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
            created_at=training.created_at,
            share_token=training.share_token,
            implementations=impl_dtos,
        )

