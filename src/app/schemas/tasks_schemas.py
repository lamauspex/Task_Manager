
""" Назначение: Схемы Tasks """


from typing import Optional
from uuid import UUID
from pydantic import Field

from src.app.schemas.base import CreateBase, OutputBase, UpdateBase
from src.app.core.constants import TaskStatus


class TaskBase(CreateBase):
    """Промежуточная модель для общей структуры задачи"""
    title: str = Field(
        max_length=100,
        min_length=1,
        description="Название задачи"
    )
    description: Optional[str] = Field(
        max_length=300,
        description="Описание задачи"
    )
    status: TaskStatus = Field(
        default=TaskStatus.CREATED,
        description="Статус задачи"
    )
    assigned_to_id: Optional[UUID] = Field(
        description="ID пользователя, кому назначена задача"
    )
    completed_by_id: Optional[UUID] = Field(
        description="ID пользователя, завершившего задачу"
    )


class TaskCreate(CreateBase):
    """ Создание задачи """
    title: str = Field(max_length=100)
    description: Optional[str] = Field(None, max_length=300)


class TaskUpdate(UpdateBase):
    """ Обновление задачи """

    description: Optional[str] = Field(
        None,
        max_length=300,
        description="Название задачи"
    )
    title: Optional[str] = Field(
        max_length=100,
        description="Описание задачи"
    )
    status: Optional[TaskStatus] = Field(
        description="Новый статус задачи"
    )

    assigned_to_id: Optional[UUID] = Field(
        description="Новое назначение задачи пользователю"
    )
    completed_by_id: Optional[UUID] = Field(
        description="Пользователь, завершивший задачу"
    )


class TaskOut(OutputBase, TaskBase):
    """ Вывод задачи """
    pass
