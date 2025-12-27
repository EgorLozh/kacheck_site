from dataclasses import dataclass
from typing import Optional


@dataclass
class RegisterUserDTO:
    """DTO for user registration."""

    email: str
    username: str
    password: str


@dataclass
class LoginUserDTO:
    """DTO for user login."""

    email: str
    password: str


@dataclass
class UserResponseDTO:
    """DTO for user response."""

    id: int
    email: str
    username: str


@dataclass
class TokenResponseDTO:
    """DTO for token response."""

    access_token: str
    token_type: str = "bearer"

