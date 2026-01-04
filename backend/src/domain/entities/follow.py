from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum


class FollowStatus(str, Enum):
    """Follow request status enum."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class Follow:
    """Follow entity (user follows another user)."""

    id: Optional[int]
    follower_id: int
    following_id: int
    created_at: datetime
    status: FollowStatus = FollowStatus.PENDING


