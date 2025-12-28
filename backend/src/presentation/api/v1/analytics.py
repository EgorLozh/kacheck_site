from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from datetime import datetime, date

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories import TrainingRepositoryImpl, UserBodyMetricRepositoryImpl
from src.domain.services.analytics_service import AnalyticsService
from src.domain.entities.training import Training
from src.domain.entities.set import Set
from src.presentation.api.dependencies import get_current_user_id

router = APIRouter(prefix="/analytics", tags=["analytics"])


def get_training_repository(db: Session = Depends(get_db)) -> TrainingRepositoryImpl:
    """Dependency to get training repository."""
    return TrainingRepositoryImpl(db)


def get_body_metric_repository(db: Session = Depends(get_db)) -> UserBodyMetricRepositoryImpl:
    """Dependency to get body metric repository."""
    return UserBodyMetricRepositoryImpl(db)


@router.get("/weight-progress")
async def get_weight_progress(
    exercise_id: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get weight progress for a specific exercise."""
    # Adjust dates to beginning/end of day to include all trainings
    if start_date:
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    if end_date:
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    
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
    # Adjust dates to beginning/end of day to include all trainings
    if start_date:
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    if end_date:
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    
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


@router.get("/training-frequency")
async def get_training_frequency(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get training frequency over time (number of trainings per date)."""
    # Adjust dates to beginning/end of day to include all trainings
    if start_date:
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    if end_date:
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    training_repository = get_training_repository(db)
    trainings = training_repository.get_all(
        user_id=current_user_id, start_date=start_date, end_date=end_date
    )

    frequency = AnalyticsService.get_training_frequency(trainings)

    return {
        "frequency": {str(d): count for d, count in sorted(frequency.items())},
    }


@router.get("/total-volume")
async def get_total_volume(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get total volume over time (all exercises combined)."""
    # Adjust dates to beginning/end of day to include all trainings
    if start_date:
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    if end_date:
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    training_repository = get_training_repository(db)
    trainings = training_repository.get_all(
        user_id=current_user_id, start_date=start_date, end_date=end_date
    )

    volume_by_date = AnalyticsService.get_total_volume_by_date(trainings)

    return {
        "volume": {str(d): round(vol, 2) for d, vol in sorted(volume_by_date.items())},
    }


@router.get("/summary")
async def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get summary analytics (total trainings, total volume, etc.)."""
    training_repository = get_training_repository(db)
    trainings = training_repository.get_all(user_id=current_user_id)

    total_trainings = len(trainings)
    
    total_volume = 0.0
    completed_trainings = [t for t in trainings if t.status.value == "completed"]
    for training in completed_trainings:
        for impl in training.implementations:
            total_volume += AnalyticsService.calculate_volume(impl.sets)

    return {
        "total_trainings": total_trainings,
        "completed_trainings": len(completed_trainings),
        "total_volume": round(total_volume, 2),
    }


@router.get("/user-weight-progress")
async def get_user_weight_progress(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get user weight progress over time."""
    body_metric_repository = get_body_metric_repository(db)
    metrics = body_metric_repository.get_by_user_id(
        user_id=current_user_id,
        start_date=start_date,
        end_date=end_date,
    )

    progress = AnalyticsService.get_weight_progress_from_metrics(metrics)

    return {
        "progress": {str(d): round(weight, 2) for d, weight in sorted(progress.items())},
    }


@router.get("/user-bmi-progress")
async def get_user_bmi_progress(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get user BMI progress over time."""
    body_metric_repository = get_body_metric_repository(db)
    metrics = body_metric_repository.get_by_user_id(
        user_id=current_user_id,
        start_date=start_date,
        end_date=end_date,
    )

    progress = AnalyticsService.get_bmi_progress_from_metrics(metrics)

    return {
        "progress": {str(d): round(bmi, 2) for d, bmi in sorted(progress.items())},
    }


