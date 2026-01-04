from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class CreateBodyMetricDTO:
    """DTO for creating a body metric entry."""

    weight: Optional[float] = None  # Weight in kg
    height: Optional[float] = None  # Height in cm
    date: Optional[date] = None  # Date of measurement, defaults to today


@dataclass
class BodyMetricResponseDTO:
    """DTO for body metric response."""

    id: int
    user_id: int
    weight: Optional[float]
    height: Optional[float]
    date: date


@dataclass
class UpdateUserProfileDTO:
    """DTO for updating user profile (current weight and height)."""

    weight: Optional[float] = None  # Weight in kg
    height: Optional[float] = None  # Height in cm




