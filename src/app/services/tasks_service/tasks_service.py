
""" Назначение: Сервис для работы с задачами """


from typing import List, Optional
from uuid import UUID

from src.app.core.constants import TaskStatus
from src.app.interfaces.i_service import ITaskService
from src.app.repositories.tasks_repo import TasksRepository
from src.app.models.tasks_models import Task
from src.app.schemas.tasks_schemas import TaskCreate, TaskOut


class TasksService(ITaskService):

    def __init__(self, repository: TasksRepository):
        self.repository = repository

    async def assign_task(
        self,
        task_id: UUID,
        user_id: UUID
    ) -> Optional[TaskOut]:
        """Назначаем задачу пользователю"""
        task = await self.repository.find_by_id(task_id)

        if task is None or task.status != TaskStatus.CREATED:
            return None

        task.assigned_to_id = user_id
        await self.repository.update(task.id, {'assigned_to_id': user_id})
        return TaskOut.model_validate(task)

    async def complete_task(
        self,
        task_id: UUID,
        user_id: UUID
    ) -> Optional[TaskOut]:
        """Отмечаем задачу как завершённую"""

        task = await self.repository.find_by_id(task_id)

        if task is None:
            return None

        task.status = TaskStatus.COMPLETED
        task.completed_by_id = user_id
        await self.repository.update(task.id, {
            'status': TaskStatus.COMPLETED.value,
            'completed_by_id': user_id
        })
        return TaskOut.model_validate(task)

    async def add(self, task_data: TaskCreate) -> TaskOut:
        """ Создание новой задачи """
        new_task = await self.repository.add(Task(**task_data.model_dump()))
        return TaskOut.model_validate(new_task)

    async def find_by_id(self, entity_id: UUID) -> Optional[TaskOut]:
        """ Получение задачи по ID """
        task = await self.repository.find_by_id(entity_id)
        return TaskOut.model_validate(task)

    async def all(self) -> List[TaskOut]:
        """ Получение списка всех задач """
        tasks = await self.repository.find_all()
        return [TaskOut.model_validate(t) for t in tasks]

    async def update(self, entity_id: UUID,
                     updated_data: dict) -> Optional[TaskOut]:
        """ Обновление задачи """
        updated_task = await self.repository.update(entity_id, updated_data)
        return TaskOut.model_validate(updated_task)

    async def delete(self, entity_id: UUID) -> bool:
        """ Удаление задачи """
        deleted = await self.repository.remove(entity_id)
        return deleted
