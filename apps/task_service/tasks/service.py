"""
Task service — business logic layer.

Rules:
  - Only CREATED tasks can be assigned.
  - Only assigned user or admin can complete a task.
  - Notifications are dispatched via NotificationService after state changes.
"""

import uuid
from typing import Optional

from backend.src.app.core.constants import TaskStatus, Role
from backend.src.app.exceptions.http import ForbiddenError, NotFoundError, UnprocessableError
from backend.src.app.models.task import Task
from backend.src.app.models.user import User
from backend.src.app.repositories.task import TaskRepository
from backend.src.app.repositories.user import UserRepository
from backend.src.app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from backend.src.app.services.notifications.service import NotificationService


class TaskService:
    def __init__(
        self,
        task_repo: TaskRepository,
        user_repo: UserRepository,
        notification_service: NotificationService,
    ) -> None:
        self._tasks = task_repo
        self._users = user_repo
        self._notify = notification_service

    # ── Read ──────────────────────────────────────────────────────────────────

    async def get_by_id(self, task_id: uuid.UUID) -> TaskOut:
        task = await self._tasks.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task", str(task_id))
        return TaskOut.model_validate(task)

    async def get_all(self) -> list[TaskOut]:
        tasks = await self._tasks.get_all()
        return [TaskOut.model_validate(t) for t in tasks]

    # ── Write ─────────────────────────────────────────────────────────────────

    async def create(self, data: TaskCreate, created_by: User) -> TaskOut:
        task = Task(
            title=data.title,
            description=data.description,
            created_by_id=created_by.id,
        )
        task = await self._tasks.add(task)
        return TaskOut.model_validate(task)

    async def update(self, task_id: uuid.UUID, data: TaskUpdate, actor: User) -> TaskOut:
        task = await self._tasks.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task", str(task_id))

        updates = data.model_dump(exclude_unset=True)
        task = await self._tasks.update_fields(task, **updates)
        return TaskOut.model_validate(task)

    async def delete(self, task_id: uuid.UUID, actor: User) -> None:
        task = await self._tasks.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task", str(task_id))
        if actor.role != Role.ADMIN and task.created_by_id != actor.id:
            raise ForbiddenError("Only task creator or admin can delete a task")
        await self._tasks.delete(task)

    async def assign(self, task_id: uuid.UUID, assignee_id: uuid.UUID, actor: User) -> TaskOut:
        task = await self._tasks.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task", str(task_id))
        if task.status != TaskStatus.CREATED:
            raise UnprocessableError("Only CREATED tasks can be assigned")

        assignee = await self._users.get_by_id(assignee_id)
        if not assignee:
            raise NotFoundError("User", str(assignee_id))

        task = await self._tasks.update_fields(
            task,
            assigned_to_id=assignee_id,
            status=TaskStatus.IN_PROGRESS,
        )

        # Fire-and-forget notification
        await self._notify.notify_task_assigned(task, assignee)

        return TaskOut.model_validate(task)

    async def complete(self, task_id: uuid.UUID, actor: User) -> TaskOut:
        task = await self._tasks.get_by_id(task_id)
        if not task:
            raise NotFoundError("Task", str(task_id))
        if task.status == TaskStatus.COMPLETED:
            raise UnprocessableError("Task is already completed")
        if actor.role != Role.ADMIN and task.assigned_to_id != actor.id:
            raise ForbiddenError("Only the assigned user or admin can complete a task")

        task = await self._tasks.update_fields(
            task,
            status=TaskStatus.COMPLETED,
            completed_by_id=actor.id,
        )
        return TaskOut.model_validate(task)
