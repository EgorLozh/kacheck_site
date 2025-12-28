from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class CreateBodyMetricRequest(BaseModel):
    """Request schema for creating a body metric entry."""

    weight: Optional[float] = Field(default=None, description="Weight in kg", ge=0, le=500)
    height: Optional[float] = Field(default=None, description="Height in cm", ge=0, le=300)
    date: Optional[date] = None  # Date of measurement (defaults to today)


class BodyMetricResponse(BaseModel):
    """Response schema for body metric."""

    id: int
    user_id: int
    weight: Optional[float]
    height: Optional[float]
    date: date

    class Config:
        from_attributes = True


class UpdateUserProfileRequest(BaseModel):
    """Request schema for updating user profile."""

    weight: Optional[float] = Field(default=None, description="Current weight in kg", ge=0, le=500)
    height: Optional[float] = Field(default=None, description="Current height in cm", ge=0, le=300)

