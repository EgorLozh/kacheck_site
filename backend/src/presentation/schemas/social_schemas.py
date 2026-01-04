from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class FollowResponse(BaseModel):
    """Schema for follow response."""

    id: int
    follower_id: int
    following_id: int
    status: str  # pending, approved, rejected
    created_at: datetime
    follower_username: Optional[str] = None
    following_username: Optional[str] = None

    class Config:
        from_attributes = True


class ReactionType(str):
    """Reaction type enum for Pydantic."""

    LIKE = "LIKE"
    LOVE = "LOVE"
    FIRE = "FIRE"
    MUSCLE = "MUSCLE"
    TARGET = "TARGET"


class ReactionRequest(BaseModel):
    """Schema for adding a reaction."""

    reaction_type: str


class ReactionResponse(BaseModel):
    """Schema for reaction response."""

    id: int
    training_id: int
    user_id: int
    reaction_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class CommentRequest(BaseModel):
    """Schema for adding a comment."""

    text: str


class CommentResponse(BaseModel):
    """Schema for comment response."""

    id: int
    training_id: int
    user_id: int
    username: Optional[str] = None
    text: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


