"""Domain constants and enumerations."""

from enum import StrEnum


class TaskStatus(StrEnum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Role(StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"
