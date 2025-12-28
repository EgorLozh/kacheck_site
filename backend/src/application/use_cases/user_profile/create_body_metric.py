from datetime import date, datetime

from src.domain.entities.user_body_metric import UserBodyMetric
from src.domain.repositories.user_body_metric_repository import IUserBodyMetricRepository
from src.domain.repositories.user_repository import IUserRepository
from src.application.dto.user_body_metric_dto import CreateBodyMetricDTO, BodyMetricResponseDTO


class CreateBodyMetricUseCase:
    """Use case for creating a body metric entry."""

    def __init__(
        self,
        body_metric_repository: IUserBodyMetricRepository,
        user_repository: IUserRepository,
    ):
        self.body_metric_repository = body_metric_repository
        self.user_repository = user_repository

    def execute(self, dto: CreateBodyMetricDTO, user_id: int) -> BodyMetricResponseDTO:
        """Create a new body metric entry and update user's current weight/height."""
        if dto.weight is None and dto.height is None:
            raise ValueError("At least one of weight or height must be provided")

        measurement_date = dto.date if dto.date else date.today()
        now = datetime.utcnow()

        body_metric = UserBodyMetric(
            id=None,
            user_id=user_id,
            weight=dto.weight,
            height=dto.height,
            date=measurement_date,
            created_at=now,
            updated_at=now,
        )

        created_metric = self.body_metric_repository.create(body_metric)

        # Update user's current weight and height if provided
        user = self.user_repository.get_by_id(user_id)
        if user:
            if dto.weight is not None:
                user.weight = dto.weight
            if dto.height is not None:
                user.height = dto.height
            user.updated_at = now
            self.user_repository.update(user)

        return BodyMetricResponseDTO(
            id=created_metric.id,
            user_id=created_metric.user_id,
            weight=created_metric.weight,
            height=created_metric.height,
            date=created_metric.date,
        )

