from dataclasses import dataclass
from typing import Optional, List


@dataclass
class CreateExerciseDTO:
    """DTO for creating an exercise."""

    name: str
    description: Optional[str]
    muscle_group_ids: List[int]
    image_path: Optional[str] = None


@dataclass
class UpdateExerciseDTO:
    """DTO for updating an exercise."""

    name: Optional[str] = None
    description: Optional[str] = None
    muscle_group_ids: Optional[List[int]] = None
    image_path: Optional[str] = None


@dataclass
class ExerciseResponseDTO:
    """DTO for exercise response."""

    id: int
    name: str
    description: Optional[str]
    image_path: Optional[str]
    is_custom: bool
    user_id: Optional[int]
    muscle_group_ids: List[int]



