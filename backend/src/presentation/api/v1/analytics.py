from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from datetime import datetime

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories import TrainingRepositoryImpl
from src.domain.services.analytics_service import AnalyticsService
from src.domain.entities.training import Training
from src.domain.entities.set import Set
from src.presentation.api.dependencies import get_current_user_id

router = APIRouter(prefix="/analytics", tags=["analytics"])


def get_training_repository(db: Session = Depends(get_db)) -> TrainingRepositoryImpl:
    """Dependency to get training repository."""
    return TrainingRepositoryImpl(db)


@router.get("/weight-progress")
async def get_weight_progress(
    exercise_id: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get weight progress for a specific exercise."""
    training_repository = get_training_repository(db)
    trainings = training_repository.get_all(
        user_id=current_user_id, start_date=start_date, end_date=end_date
    )

    # Filter sets by exercise_id
    sets_by_date: Dict[datetime, List[Set]] = {}
    for training in trainings:
        for impl in training.implementations:
            if impl.exercise_id == exercise_id:
                if training.date_time not in sets_by_date:
                    sets_by_date[training.date_time] = []
                sets_by_date[training.date_time].extend(impl.sets)

    progress = AnalyticsService.get_weight_progress(sets_by_date)

    return {
        "exercise_id": exercise_id,
        "progress": {str(date): weight for date, weight in progress.items()},
    }


@router.get("/volume-progress")
async def get_volume_progress(
    exercise_id: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get volume progress for a specific exercise."""
    training_repository = get_training_repository(db)
    trainings = training_repository.get_all(
        user_id=current_user_id, start_date=start_date, end_date=end_date
    )

    # Filter sets by exercise_id
    sets_by_date: Dict[datetime, List[Set]] = {}
    for training in trainings:
        for impl in training.implementations:
            if impl.exercise_id == exercise_id:
                if training.date_time not in sets_by_date:
                    sets_by_date[training.date_time] = []
                sets_by_date[training.date_time].extend(impl.sets)

    progress = AnalyticsService.get_volume_progress(sets_by_date)

    return {
        "exercise_id": exercise_id,
        "progress": {str(date): volume for date, volume in progress.items()},
    }


@router.get("/one-rep-max")
async def calculate_one_rep_max(
    weight: float = Query(..., description="Weight used"),
    reps: int = Query(..., description="Number of repetitions"),
    formula: str = Query("brzycki", description="Formula to use (brzycki, epley, lombardi)"),
):
    """Calculate one-rep maximum (1RM)."""
    try:
        one_rm = AnalyticsService.calculate_one_rep_max(weight, reps, formula)
        return {
            "weight": weight,
            "reps": reps,
            "formula": formula,
            "one_rep_max": round(one_rm, 2),
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

