from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RPE:
    """Value object for Rate of Perceived Exertion (1-10 scale)."""

    value: int

    def __post_init__(self):
        if not (1 <= self.value <= 10):
            raise ValueError("RPE must be between 1 and 10")

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def optional(cls, value: Optional[int]) -> Optional["RPE"]:
        """Create optional RPE from optional int."""
        if value is None:
            return None
        return cls(value)





