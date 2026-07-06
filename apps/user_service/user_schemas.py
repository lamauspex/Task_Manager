"""User schemas."""

from typing import Optional
from pydantic import ConfigDict, EmailStr, Field, computed_field, field_validator

from backend.src.app.core.constants import Role
from backend.src.app.schemas.base import BaseSchema, TimestampedSchema


class UserCreate(BaseSchema):
    """Input schema for registration."""

    model_config = ConfigDict(str_to_lower=True, str_strip_whitespace=True)

    first_name: str = Field(min_length=2, max_length=50, examples=["Кирилл"])
    last_name: str = Field(min_length=2, max_length=50, examples=["Резник"])
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    role: Role = Role.USER

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isalpha() for c in v):
            raise ValueError("Password must contain at least one letter")
        return v


class UserUpdate(BaseSchema):
    """Partial update schema."""

    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None


class UserOut(TimestampedSchema):
    """Full user output (used in admin / self-profile)."""

    first_name: str
    last_name: str
    email: EmailStr
    role: Role
    is_active: bool

    @field_validator("role", mode="before")
    @classmethod
    def coerce_role(cls, v) -> Role:
        return Role(v) if isinstance(v, str) else v

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class UserPublic(BaseSchema):
    """Minimal public user info (embedded in task responses)."""

    id: str
    full_name: str
    email: EmailStr
