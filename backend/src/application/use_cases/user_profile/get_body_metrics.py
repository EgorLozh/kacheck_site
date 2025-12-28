from typing import List
from datetime import date
from typing import Optional

from src.domain.repositories.user_body_metric_repository import IUserBodyMetricRepository
from src.application.dto.user_body_metric_dto import BodyMetricResponseDTO


class GetBodyMetricsUseCase:
    """Use case for getting body metrics."""

    def __init__(self, body_metric_repository: IUserBodyMetricRepository):
        self.body_metric_repository = body_metric_repository

    def execute(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[BodyMetricResponseDTO]:
        """Get all body metrics for a user, optionally filtered by date range."""
        metrics = self.body_metric_repository.get_by_user_id(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        return [
            BodyMetricResponseDTO(
                id=metric.id,
                user_id=metric.user_id,
                weight=metric.weight,
                height=metric.height,
                date=metric.date,
            )
            for metric in metrics
        ]

