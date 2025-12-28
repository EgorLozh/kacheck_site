from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from datetime import datetime, date

from src.infrastructure.database.session import get_db
from src.infrastructure.repositories import (
    TrainingRepositoryImpl,
    UserBodyMetricRepositoryImpl,
    ExerciseRepositoryImpl,
    MuscleGroupRepositoryImpl,
)
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


def get_exercise_repository(db: Session = Depends(get_db)) -> ExerciseRepositoryImpl:
    """Dependency to get exercise repository."""
    return ExerciseRepositoryImpl(db)


def get_muscle_group_repository(db: Session = Depends(get_db)) -> MuscleGroupRepositoryImpl:
    """Dependency to get muscle group repository."""
    return MuscleGroupRepositoryImpl(db)


def adjust_date_range(start_date: Optional[datetime], end_date: Optional[datetime]) -> tuple[Optional[datetime], Optional[datetime]]:
    """
    Adjust date range to include full days.
    start_date is set to 00:00:00, end_date is set to 23:59:59.999999
    """
    if start_date:
        # Ensure start_date is at the beginning of the day
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    if end_date:
        # Set to end of day to include the entire last day (e.g., if end_date is 2024-01-28, include all of 28th)
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start_date, end_date


@router.get("/weight-progress")
async def get_weight_progress(
    exercise_id: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get weight progress for a specific exercise."""
    start_date, end_date = adjust_date_range(start_date, end_date)
    
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
    start_date, end_date = adjust_date_range(start_date, end_date)
    
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
    start_date, end_date = adjust_date_range(start_date, end_date)
    
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
    start_date, end_date = adjust_date_range(start_date, end_date)
    
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


@router.get("/streak")
async def get_training_streak(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get current training streak (consecutive days with at least one completed training)."""
    training_repository = get_training_repository(db)
    trainings = training_repository.get_all(user_id=current_user_id)

    streak = AnalyticsService.get_training_streak(trainings)

    return {
        "streak": streak,
    }


@router.get("/prs")
async def get_all_prs(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
    limit: Optional[int] = Query(10, description="Maximum number of PRs to return"),
):
    """Get all personal records (PRs) - maximum weight for each exercise."""
    training_repository = get_training_repository(db)
    exercise_repository = get_exercise_repository(db)
    trainings = training_repository.get_all(user_id=current_user_id)

    prs = AnalyticsService.get_all_prs(trainings)

    # Enrich with exercise names
    enriched_prs = []
    for pr in prs[:limit]:
        exercise = exercise_repository.get_by_id(pr['exercise_id'])
        if exercise:
            enriched_prs.append({
                'exercise_id': pr['exercise_id'],
                'exercise_name': str(exercise.name),
                'weight': pr['weight'],
                'reps': pr['reps'],
                'date': str(pr['date']),
                'training_id': pr['training_id'],
            })

    return {
        "prs": enriched_prs,
    }


@router.get("/exercise/{exercise_id}/pr")
async def get_exercise_pr(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get personal record (PR) for a specific exercise."""
    training_repository = get_training_repository(db)
    exercise_repository = get_exercise_repository(db)
    trainings = training_repository.get_all(user_id=current_user_id)

    pr = AnalyticsService.get_exercise_pr(trainings, exercise_id)
    
    if not pr:
        return {
            "exercise_id": exercise_id,
            "pr": None,
        }

    # Enrich with exercise name
    exercise = exercise_repository.get_by_id(exercise_id)
    exercise_name = str(exercise.name) if exercise else None

    return {
        "exercise_id": exercise_id,
        "exercise_name": exercise_name,
        "pr": {
            "weight": pr['weight'],
            "reps": pr['reps'],
            "date": str(pr['date']),
            "training_id": pr['training_id'],
        },
    }


@router.get("/exercise/{exercise_id}/1rm-progress")
async def get_exercise_1rm_progress(
    exercise_id: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    formula: str = Query("brzycki", description="Formula to use (brzycki, epley, lombardi)"),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get 1RM progress for a specific exercise."""
    start_date, end_date = adjust_date_range(start_date, end_date)
    
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

    progress = AnalyticsService.get_1rm_progress(sets_by_date, formula)

    return {
        "exercise_id": exercise_id,
        "formula": formula,
        "progress": {str(date): round(one_rm, 2) for date, one_rm in sorted(progress.items())},
    }


@router.get("/muscle-groups/volume")
async def get_muscle_group_volume(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get total volume by muscle group."""
    start_date, end_date = adjust_date_range(start_date, end_date)
    
    training_repository = get_training_repository(db)
    exercise_repository = get_exercise_repository(db)
    muscle_group_repository = get_muscle_group_repository(db)
    
    trainings = training_repository.get_all(
        user_id=current_user_id, start_date=start_date, end_date=end_date
    )

    volume_by_group = AnalyticsService.get_muscle_group_volume(trainings, exercise_repository)

    # Enrich with muscle group names
    result = []
    for muscle_group_id, volume in volume_by_group.items():
        muscle_group = muscle_group_repository.get_by_id(muscle_group_id)
        if muscle_group:
            result.append({
                "muscle_group_id": muscle_group_id,
                "muscle_group_name": muscle_group.name,
                "volume": round(volume, 2),
            })

    # Sort by volume descending
    result.sort(key=lambda x: x['volume'], reverse=True)

    return {
        "volume_by_group": result,
    }


@router.get("/muscle-groups/frequency")
async def get_muscle_group_frequency(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    """Get training frequency by muscle group."""
    start_date, end_date = adjust_date_range(start_date, end_date)
    
    training_repository = get_training_repository(db)
    exercise_repository = get_exercise_repository(db)
    muscle_group_repository = get_muscle_group_repository(db)
    
    trainings = training_repository.get_all(
        user_id=current_user_id, start_date=start_date, end_date=end_date
    )

    frequency_by_group = AnalyticsService.get_muscle_group_frequency(trainings, exercise_repository)

    # Enrich with muscle group names
    result = []
    for muscle_group_id, frequency in frequency_by_group.items():
        muscle_group = muscle_group_repository.get_by_id(muscle_group_id)
        if muscle_group:
            result.append({
                "muscle_group_id": muscle_group_id,
                "muscle_group_name": muscle_group.name,
                "frequency": frequency,
            })

    # Sort by frequency descending
    result.sort(key=lambda x: x['frequency'], reverse=True)

    return {
        "frequency_by_group": result,
    }


