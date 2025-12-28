from dataclasses import dataclass


@dataclass(frozen=True)
class ExerciseName:
    """Value object for exercise name."""

    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Exercise name cannot be empty")
        if len(self.value.strip()) > 255:
            raise ValueError("Exercise name must be less than 255 characters")

    def __str__(self) -> str:
        return self.value.strip()



