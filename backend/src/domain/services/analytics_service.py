from typing import List, Dict, Optional
from datetime import datetime

from ..entities.set import Set


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

