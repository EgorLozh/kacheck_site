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

    @staticmethod
    def get_training_streak(trainings: List[Training]) -> int:
        """
        Calculate current training streak (consecutive days with at least one completed training).

        Args:
            trainings: List of trainings

        Returns:
            Current streak in days (0 if no trainings or streak is broken)
        """
        if not trainings:
            return 0

        # Filter only completed trainings
        completed_trainings = [t for t in trainings if t.status.value == "completed"]
        if not completed_trainings:
            return 0

        # Get unique training dates (only date part, not time)
        training_dates = set()
        for training in completed_trainings:
            training_date = training.date_time.date() if isinstance(training.date_time, datetime) else training.date_time
            training_dates.add(training_date)

        # Sort dates in descending order
        sorted_dates = sorted(training_dates, reverse=True)
        if not sorted_dates:
            return 0

        # Calculate streak from the most recent training date backwards
        today = date.today()
        yesterday = date.fromordinal(today.toordinal() - 1)
        
        # Start from the most recent training date
        most_recent_date = sorted_dates[0]
        
        # If the most recent training was more than 1 day ago, streak is broken
        days_ago = (today - most_recent_date).days
        if days_ago > 1:
            return 0
        
        # Calculate consecutive days from most recent date backwards
        streak = 1
        current_date = most_recent_date
        
        # Go backwards day by day
        for i in range(1, len(sorted_dates)):
            expected_date = date.fromordinal(current_date.toordinal() - 1)
            if expected_date in sorted_dates:
                streak += 1
                current_date = expected_date
            else:
                break
        
        return streak

    @staticmethod
    def get_exercise_pr(trainings: List[Training], exercise_id: int) -> Optional[Dict]:
        """
        Get personal record (PR) for a specific exercise (maximum weight used).

        Args:
            trainings: List of trainings
            exercise_id: ID of the exercise

        Returns:
            Dictionary with PR info: {'weight': float, 'reps': int, 'date': date, 'training_id': int}
            or None if no PR found
        """
        if not trainings:
            return None

        # Filter only completed trainings
        completed_trainings = [t for t in trainings if t.status.value == "completed"]
        if not completed_trainings:
            return None

        max_weight = 0.0
        pr_info = None

        for training in completed_trainings:
            for impl in training.implementations:
                if impl.exercise_id == exercise_id:
                    for set_entity in impl.sets:
                        weight = float(set_entity.weight.value)
                        reps = int(set_entity.reps.value)
                        if weight > max_weight:
                            max_weight = weight
                            training_date = training.date_time.date() if isinstance(training.date_time, datetime) else training.date_time
                            pr_info = {
                                'weight': weight,
                                'reps': reps,
                                'date': training_date,
                                'training_id': training.id,
                            }

        return pr_info

    @staticmethod
    def get_all_prs(trainings: List[Training]) -> List[Dict]:
        """
        Get all personal records (PRs) - maximum weight for each exercise.

        Args:
            trainings: List of trainings

        Returns:
            List of dictionaries with PR info: [{'exercise_id': int, 'weight': float, 'reps': int, 'date': date, 'training_id': int}, ...]
        """
        if not trainings:
            return []

        # Filter only completed trainings
        completed_trainings = [t for t in trainings if t.status.value == "completed"]
        if not completed_trainings:
            return []

        # Dictionary to track max weight per exercise
        exercise_prs: Dict[int, Dict] = {}

        for training in completed_trainings:
            training_date = training.date_time.date() if isinstance(training.date_time, datetime) else training.date_time
            for impl in training.implementations:
                exercise_id = impl.exercise_id
                for set_entity in impl.sets:
                    weight = float(set_entity.weight.value)
                    reps = int(set_entity.reps.value)
                    
                    # Check if this is a new PR for this exercise
                    if exercise_id not in exercise_prs or weight > exercise_prs[exercise_id]['weight']:
                        exercise_prs[exercise_id] = {
                            'exercise_id': exercise_id,
                            'weight': weight,
                            'reps': reps,
                            'date': training_date,
                            'training_id': training.id,
                        }

        # Sort by weight descending and return top results
        prs_list = list(exercise_prs.values())
        prs_list.sort(key=lambda x: x['weight'], reverse=True)
        
        return prs_list

    @staticmethod
    def get_muscle_group_volume(trainings: List[Training], exercise_repository) -> Dict[int, float]:
        """
        Get total volume by muscle group.

        Args:
            trainings: List of trainings
            exercise_repository: Exercise repository to get exercise details

        Returns:
            Dictionary mapping muscle_group_id to total volume
        """
        if not trainings:
            return {}

        # Filter only completed trainings
        completed_trainings = [t for t in trainings if t.status.value == "completed"]
        if not completed_trainings:
            return {}

        muscle_group_volume: Dict[int, float] = defaultdict(float)

        for training in completed_trainings:
            for impl in training.implementations:
                # Get exercise to find muscle groups
                exercise = exercise_repository.get_by_id(impl.exercise_id)
                if exercise:
                    # Calculate volume for this implementation
                    volume = AnalyticsService.calculate_volume(impl.sets)
                    # Distribute volume across all muscle groups of this exercise
                    if exercise.muscle_group_ids:
                        volume_per_group = volume / len(exercise.muscle_group_ids)
                        for muscle_group_id in exercise.muscle_group_ids:
                            muscle_group_volume[muscle_group_id] += volume_per_group

        return dict(muscle_group_volume)

    @staticmethod
    def get_muscle_group_frequency(trainings: List[Training], exercise_repository) -> Dict[int, int]:
        """
        Get training frequency by muscle group (number of trainings that included exercises for each group).

        Args:
            trainings: List of trainings
            exercise_repository: Exercise repository to get exercise details

        Returns:
            Dictionary mapping muscle_group_id to frequency count
        """
        if not trainings:
            return {}

        # Filter only completed trainings
        completed_trainings = [t for t in trainings if t.status.value == "completed"]
        if not completed_trainings:
            return {}

        muscle_group_frequency: Dict[int, set] = defaultdict(set)

        for training in completed_trainings:
            training_date = training.date_time.date() if isinstance(training.date_time, datetime) else training.date_time
            for impl in training.implementations:
                exercise = exercise_repository.get_by_id(impl.exercise_id)
                if exercise:
                    for muscle_group_id in exercise.muscle_group_ids:
                        # Use set to count unique training dates per muscle group
                        muscle_group_frequency[muscle_group_id].add(training_date)

        # Convert sets to counts
        return {mg_id: len(dates) for mg_id, dates in muscle_group_frequency.items()}

    @staticmethod
    def get_1rm_progress(sets_by_date: Dict[datetime, List[Set]], formula: str = "brzycki") -> Dict[datetime, float]:
        """
        Get 1RM progress over time (estimated one-rep max per date).

        Args:
            sets_by_date: Dictionary mapping dates to lists of sets
            formula: Formula to use for 1RM calculation (default: "brzycki")

        Returns:
            Dictionary mapping dates to estimated 1RM values
        """
        progress = {}
        for date, sets in sets_by_date.items():
            if sets:
                # Calculate 1RM for each set and take the maximum
                max_1rm = 0.0
                for set_entity in sets:
                    weight = float(set_entity.weight.value)
                    reps = int(set_entity.reps.value)
                    if reps > 0:
                        try:
                            one_rm = AnalyticsService.calculate_one_rep_max(weight, reps, formula)
                            max_1rm = max(max_1rm, one_rm)
                        except ValueError:
                            continue
                if max_1rm > 0:
                    progress[date] = max_1rm
        return progress


