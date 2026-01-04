from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum


class ReactionType(str, Enum):
    """Reaction type enum."""

    LIKE = "LIKE"  # 👍
    LOVE = "LOVE"  # ❤️
    FIRE = "FIRE"  # 🔥
    MUSCLE = "MUSCLE"  # 💪
    TARGET = "TARGET"  # 🎯


@dataclass
class TrainingReaction:
    """Training reaction entity."""

    id: Optional[int]
    training_id: int
    user_id: int
    reaction_type: ReactionType
    created_at: datetime


