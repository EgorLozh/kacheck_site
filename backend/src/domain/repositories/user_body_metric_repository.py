from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import date, datetime

from ..entities.user_body_metric import UserBodyMetric


class IUserBodyMetricRepository(ABC):
    """Interface for UserBodyMetric repository (Port)."""

    @abstractmethod
    def create(self, body_metric: UserBodyMetric) -> UserBodyMetric:
        """Create a new body metric entry."""
        pass

    @abstractmethod
    def get_by_id(self, metric_id: int) -> Optional[UserBodyMetric]:
        """Get body metric by ID."""
        pass

    @abstractmethod
    def get_by_user_id(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[UserBodyMetric]:
        """Get all body metrics for a user, optionally filtered by date range."""
        pass

    @abstractmethod
    def get_latest_by_user_id(self, user_id: int) -> Optional[UserBodyMetric]:
        """Get the latest body metric entry for a user."""
        pass

    @abstractmethod
    def update(self, body_metric: UserBodyMetric) -> UserBodyMetric:
        """Update body metric."""
        pass

    @abstractmethod
    def delete(self, metric_id: int) -> None:
        """Delete body metric."""
        pass

