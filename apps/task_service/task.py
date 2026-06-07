"""Task repository."""

import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.src.app.core.constants import TaskStatus
from backend.src.app.models.task import Task
from backend.src.app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    model_class = Task

    async def get_by_id_with_relations(self, task_id: uuid.UUID) -> Optional[Task]:
        result = await self._session.execute(
            select(Task)
            .where(Task.id == task_id)
            .options(
                selectinload(Task.assigned_to),
                selectinload(Task.completed_by),
                selectinload(Task.created_by),
            )
        )
        return result.scalar_one_or_none()

    async def get_all_by_status(self, status: TaskStatus) -> list[Task]:
        result = await self._session.execute(
            select(Task).where(Task.status == status)
        )
        return list(result.scalars().all())

    async def get_assigned_to_user(self, user_id: uuid.UUID) -> list[Task]:
        result = await self._session.execute(
            select(Task).where(Task.assigned_to_id == user_id)
        )
        return list(result.scalars().all())

    async def update_fields(self, task: Task, **fields) -> Task:
        for key, value in fields.items():
            setattr(task, key, value)
        await self._session.flush()
        await self._session.refresh(task)
        return task
