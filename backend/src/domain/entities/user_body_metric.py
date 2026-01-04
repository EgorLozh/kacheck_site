from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class UserBodyMetric:
    """User body metric entity (weight and height tracking)."""

    id: Optional[int]
    user_id: int
    weight: Optional[float]  # Weight in kg
    height: Optional[float]  # Height in cm
    date: date  # Date of measurement
    created_at: datetime
    updated_at: datetime




