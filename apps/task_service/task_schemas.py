"""Task schemas."""

import uuid
from typing import Optional
from pydantic import Field, ConfigDict

from backend.src.app.core.constants import TaskStatus
from backend.src.app.schemas.base import BaseSchema, TimestampedSchema


class TaskCreate(BaseSchema):
    title: str = Field(min_length=1, max_length=100, examples=["Написать тесты"])
    description: Optional[str] = Field(None, max_length=500)


class TaskUpdate(BaseSchema):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus] = None
    assigned_to_id: Optional[uuid.UUID] = None


class TaskOut(TimestampedSchema):
    title: str
    description: Optional[str]
    status: TaskStatus
    assigned_to_id: Optional[uuid.UUID]
    completed_by_id: Optional[uuid.UUID]
    created_by_id: Optional[uuid.UUID]
