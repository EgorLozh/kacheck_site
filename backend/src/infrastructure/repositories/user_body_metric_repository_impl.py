from typing import Optional, List
from datetime import date, datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.domain.entities.user_body_metric import UserBodyMetric
from src.domain.repositories.user_body_metric_repository import IUserBodyMetricRepository
from src.infrastructure.database.models.user_body_metric_model import UserBodyMetricModel


class UserBodyMetricRepositoryImpl(IUserBodyMetricRepository):
    """SQLAlchemy implementation of UserBodyMetric repository (Adapter)."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, body_metric: UserBodyMetric) -> UserBodyMetric:
        """Create a new body metric entry."""
        db_metric = UserBodyMetricModel(
            user_id=body_metric.user_id,
            weight=body_metric.weight,
            height=body_metric.height,
            date=body_metric.date,
            created_at=body_metric.created_at,
            updated_at=body_metric.updated_at,
        )
        self.db.add(db_metric)
        self.db.commit()
        self.db.refresh(db_metric)
        return self._to_entity(db_metric)

    def get_by_id(self, metric_id: int) -> Optional[UserBodyMetric]:
        """Get body metric by ID."""
        db_metric = self.db.query(UserBodyMetricModel).filter(UserBodyMetricModel.id == metric_id).first()
        return self._to_entity(db_metric) if db_metric else None

    def get_by_user_id(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[UserBodyMetric]:
        """Get all body metrics for a user, optionally filtered by date range."""
        query = self.db.query(UserBodyMetricModel).filter(UserBodyMetricModel.user_id == user_id)

        if start_date:
            query = query.filter(UserBodyMetricModel.date >= start_date)
        if end_date:
            query = query.filter(UserBodyMetricModel.date <= end_date)

        query = query.order_by(UserBodyMetricModel.date.desc())
        db_metrics = query.all()
        return [self._to_entity(db_metric) for db_metric in db_metrics]

    def get_latest_by_user_id(self, user_id: int) -> Optional[UserBodyMetric]:
        """Get the latest body metric entry for a user."""
        db_metric = (
            self.db.query(UserBodyMetricModel)
            .filter(UserBodyMetricModel.user_id == user_id)
            .order_by(UserBodyMetricModel.date.desc())
            .first()
        )
        return self._to_entity(db_metric) if db_metric else None

    def update(self, body_metric: UserBodyMetric) -> UserBodyMetric:
        """Update body metric."""
        if body_metric.id is None:
            raise ValueError("Body metric id is required for update")
        db_metric = self.db.query(UserBodyMetricModel).filter(UserBodyMetricModel.id == body_metric.id).first()
        if not db_metric:
            raise ValueError(f"Body metric with id {body_metric.id} not found")

        db_metric.weight = body_metric.weight
        db_metric.height = body_metric.height
        db_metric.date = body_metric.date
        db_metric.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(db_metric)
        return self._to_entity(db_metric)

    def delete(self, metric_id: int) -> None:
        """Delete body metric."""
        db_metric = self.db.query(UserBodyMetricModel).filter(UserBodyMetricModel.id == metric_id).first()
        if db_metric:
            self.db.delete(db_metric)
            self.db.commit()

    @staticmethod
    def _to_entity(db_metric: UserBodyMetricModel) -> UserBodyMetric:
        """Convert SQLAlchemy model to domain entity."""
        return UserBodyMetric(
            id=db_metric.id,
            user_id=db_metric.user_id,
            weight=float(db_metric.weight) if db_metric.weight is not None else None,
            height=float(db_metric.height) if db_metric.height is not None else None,
            date=db_metric.date,
            created_at=db_metric.created_at,
            updated_at=db_metric.updated_at,
        )


