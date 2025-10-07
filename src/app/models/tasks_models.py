
""" Назначение: Модели задач """


from typing import Optional
from uuid import UUID
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.app.core.constants import TaskStatus
from src.app.core.database import Base
from src.app.models.base import BaseModel
from src.app.models.users_models import User


class Task(Base, BaseModel):
    """Таблица Tasks """

    title: Mapped[str] = mapped_column(
        String(length=100),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(length=300),
        nullable=True
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.CREATED
    )

    # Дополнительные поля для назначения и завершения задачи
    assigned_to_id: Mapped[Optional[UUID]
                           ] = mapped_column(ForeignKey('users.id'))
    completed_by_id: Mapped[Optional[UUID]
                            ] = mapped_column(ForeignKey('users.id'))

    # Связанные отношения
    assigned_to: Mapped['User'] = relationship(
        "User",
        foreign_keys=[assigned_to_id],
        backref='assigned_tasks'
    )
    completed_by: Mapped['User'] = relationship(
        "User",
        foreign_keys=[completed_by_id],
        backref='completed_tasks'
    )
