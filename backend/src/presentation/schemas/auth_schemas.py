from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    """Request schema for user registration."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password format."""
        # Password can be any length - we handle long passwords with SHA-256 + bcrypt
        # Just ensure it's not empty after stripping
        if not v or not v.strip():
            raise ValueError("Password cannot be empty")
        return v


class LoginRequest(BaseModel):
    """Request schema for user login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response schema for token."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Response schema for user."""

    id: int
    email: str
    username: str

    class Config:
        from_attributes = True

