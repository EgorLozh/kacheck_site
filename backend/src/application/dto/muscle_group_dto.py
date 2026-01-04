from dataclasses import dataclass


@dataclass
class CreateMuscleGroupDTO:
    """DTO for creating a muscle group."""

    name: str


@dataclass
class UpdateMuscleGroupDTO:
    """DTO for updating a muscle group."""

    name: str


@dataclass
class MuscleGroupResponseDTO:
    """DTO for muscle group response."""

    id: int
    name: str
    is_system: bool





