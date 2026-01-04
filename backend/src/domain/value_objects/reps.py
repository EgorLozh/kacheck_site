from dataclasses import dataclass


@dataclass(frozen=True)
class Reps:
    """Value object for repetitions (reps must be > 0)."""

    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Reps must be greater than 0")

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)





