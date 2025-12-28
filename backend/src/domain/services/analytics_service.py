from typing import List, Dict, Optional, Union
from datetime import datetime, date
from collections import defaultdict

from ..entities.set import Set
from ..entities.training import Training
from ..entities.user_body_metric import UserBodyMetric


class AnalyticsService:
    """Domain service for analytics calculations."""

    @staticmethod
    def calculate_one_rep_max(weight: float, reps: int, formula: str = "brzycki") -> float:
        """
        Calculate one-rep maximum (1RM) using specified formula.

        Formulas:
        - brzycki: 1RM = weight / (1.0278 - 0.0278 * reps)
        - epley: 1RM = weight * (1 + reps / 30)
        - lombardi: 1RM = weight * reps ^ 0.10

        Args:
            weight: Weight used in the set
            reps: Number of repetitions
            formula: Formula to use (default: "brzycki")

        Returns:
            Estimated one-rep maximum
        """
        if reps <= 0:
            raise ValueError("Reps must be greater than 0")
        if reps == 1:
            return weight

        if formula.lower() == "brzycki":
            return weight / (1.0278 - 0.0278 * reps)
        elif formula.lower() == "epley":
            return weight * (1 + reps / 30)
        elif formula.lower() == "lombardi":
            return weight * (reps ** 0.10)
        else:
            raise ValueError(f"Unknown formula: {formula}")

    @staticmethod
    def calculate_volume(sets: List[Set]) -> float:
        """
        Calculate total volume (weight * reps) for a list of sets.

        Args:
            sets: List of sets

        Returns:
            Total volume
        """
        return sum(float(set.weight.value) * int(set.reps.value) for set in sets)

    @staticmethod
    def get_weight_progress(sets_by_date: Dict[datetime, List[Set]]) -> Dict[datetime, float]:
        """
        Get weight progress over time (max weight per date).

        Args:
            sets_by_date: Dictionary mapping dates to lists of sets

        Returns:
            Dictionary mapping dates to max weights
        """
        progress = {}
        for date, sets in sets_by_date.items():
            if sets:
                max_weight = max(float(set.weight.value) for set in sets)
                progress[date] = max_weight
        return progress

    @staticmethod
    def get_volume_progress(sets_by_date: Dict[datetime, List[Set]]) -> Dict[datetime, float]:
        """
        Get volume progress over time (total volume per date).

        Args:
            sets_by_date: Dictionary mapping dates to lists of sets

        Returns:
            Dictionary mapping dates to total volumes
        """
        progress = {}
        for date, sets in sets_by_date.items():
            progress[date] = AnalyticsService.calculate_volume(sets)
        return progress

    @staticmethod
    def calculate_bmi(weight: float, height: float) -> float:
        """
        Calculate Body Mass Index (BMI).

        Args:
            weight: Weight in kg
            height: Height in cm

        Returns:
            BMI value
        """
        if height <= 0:
            raise ValueError("Height must be greater than 0")
        height_m = height / 100.0  # Convert cm to meters
        return weight / (height_m ** 2)

    @staticmethod
    def get_training_frequency(trainings: List[Training]) -> Dict[date, int]:
        """
        Get training frequency by date (number of trainings per date).

        Args:
            trainings: List of trainings

        Returns:
            Dictionary mapping dates to number of trainings
        """
        frequency = defaultdict(int)
        for training in trainings:
            # Extract date from datetime
            training_date = training.date_time.date() if isinstance(training.date_time, datetime) else training.date_time
            frequency[training_date] += 1
        return dict(frequency)

    @staticmethod
    def get_total_volume_by_date(trainings: List[Training]) -> Dict[date, float]:
        """
        Get total volume (all exercises combined) by date.

        Args:
            trainings: List of trainings

        Returns:
            Dictionary mapping dates to total volumes
        """
        volume_by_date = defaultdict(float)
        for training in trainings:
            training_date = training.date_time.date() if isinstance(training.date_time, datetime) else training.date_time
            total_volume = 0.0
            for impl in training.implementations:
                total_volume += AnalyticsService.calculate_volume(impl.sets)
            volume_by_date[training_date] += total_volume
        return dict(volume_by_date)

    @staticmethod
    def get_weight_progress_from_metrics(metrics: List[UserBodyMetric]) -> Dict[date, float]:
        """
        Get weight progress from body metrics.

        Args:
            metrics: List of body metrics

        Returns:
            Dictionary mapping dates to weights (only entries with weight data)
        """
        progress = {}
        for metric in metrics:
            if metric.weight is not None:
                progress[metric.date] = metric.weight
        return progress

    @staticmethod
    def get_bmi_progress_from_metrics(metrics: List[UserBodyMetric]) -> Dict[date, float]:
        """
        Get BMI progress from body metrics.

        Args:
            metrics: List of body metrics

        Returns:
            Dictionary mapping dates to BMI values (only entries with both weight and height)
        """
        progress = {}
        for metric in metrics:
            if metric.weight is not None and metric.height is not None:
                try:
                    bmi = AnalyticsService.calculate_bmi(metric.weight, metric.height)
                    progress[metric.date] = bmi
                except ValueError:
                    # Skip invalid entries
                    continue
        return progress


