
""" Назначение: Реализация репозитория задач """


from typing import List, Optional, Union
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.interfaces.i_repository import ITaskRepository
from src.app.models.tasks_models import Task
from src.app.schemas.tasks_schemas import TaskUpdate


class TasksRepository(ITaskRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, task: Task) -> Task:
        """ Добавляет новую задачу """
        self.db.add(task)
        await self.db.flush()
        await self.db.refresh(task)
        await self.db.commit()
        return task

    async def find_by_id(self, entity_id: UUID) -> Optional[Task]:
        """ Поиск по id """
        result = await self.db.execute(
            select(Task).where(Task.id == entity_id)
        )
        return result.scalar_one_or_none()

    async def find_all(self) -> List[Task]:
        """ Возвращает все задачи """
        result = await self.db.execute(select(Task))
        tasks = result.scalars().all()
        return tasks

    async def update(self, entity_id: UUID,
                     updates: Union[dict, TaskUpdate]
                     ) -> Optional[Task]:
        """ Обновляет существующее задание """
        task = await self.find_by_id(entity_id)

        if task is None:
            return None

        if isinstance(updates, TaskUpdate):
            updates = updates.model_dump(exclude_unset=True)

        for field, value in updates.items():
            setattr(task, field, value)

        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def remove(self, entity_id: UUID) -> bool:
        """ Удаляет задачу по её ID """
        task = await self.find_by_id(entity_id)
        if task is None:
            return False

        await self.db.delete(task)
        await self.db.commit()
        return True
