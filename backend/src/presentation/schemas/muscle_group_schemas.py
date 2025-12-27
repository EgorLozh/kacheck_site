from pydantic import BaseModel


class MuscleGroupBase(BaseModel):
    """Base schema for muscle group."""

    name: str


class MuscleGroupCreate(MuscleGroupBase):
    """Schema for creating muscle group."""

    pass


class MuscleGroupUpdate(MuscleGroupBase):
    """Schema for updating muscle group."""

    pass


class MuscleGroupResponse(MuscleGroupBase):
    """Schema for muscle group response."""

    id: int
    is_system: bool

    class Config:
        from_attributes = True

