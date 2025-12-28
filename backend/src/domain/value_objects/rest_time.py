from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RestTime:
    """Value object for rest time in seconds (must be >= 0)."""

    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Rest time must be greater than or equal to 0")

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def optional(cls, value: Optional[int]) -> Optional["RestTime"]:
        """Create optional RestTime from optional int."""
        if value is None:
            return None
        return cls(value)



