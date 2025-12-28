from dataclasses import dataclass
from typing import Optional, List


@dataclass
class SetTemplateDTO:
    """DTO for a set template."""

    order_index: int
    weight: Optional[float] = None
    reps: Optional[int] = None


@dataclass
class ImplementationTemplateDTO:
    """DTO for an implementation template."""

    exercise_id: int
    order_index: int
    set_templates: List[SetTemplateDTO]


@dataclass
class CreateTemplateDTO:
    """DTO for creating a training template."""

    name: str
    description: Optional[str] = None
    implementation_templates: List[ImplementationTemplateDTO] = None


@dataclass
class UpdateTemplateDTO:
    """DTO for updating a training template."""

    name: Optional[str] = None
    description: Optional[str] = None
    implementation_templates: Optional[List[ImplementationTemplateDTO]] = None


@dataclass
class TemplateResponseDTO:
    """DTO for training template response."""

    id: int
    name: str
    description: Optional[str]
    user_id: Optional[int]
    implementation_templates: List[ImplementationTemplateDTO]


