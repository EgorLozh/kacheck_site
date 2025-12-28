from dataclasses import dataclass


@dataclass(frozen=True)
class Weight:
    """Value object for weight (weight must be >= 0, 0 for bodyweight exercises)."""

    value: float

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Weight must be greater than or equal to 0")

    def __float__(self) -> float:
        return self.value

    def __str__(self) -> str:
        return str(self.value)


