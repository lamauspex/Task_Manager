
""" Назначение: Вспомогательные методы """


from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.repositories.tasks_repo import TasksRepository
from src.app.repositories.users_repo import UsersRepository
from src.app.services.tasks_service.tasks_service import TasksService
from src.app.services.users_services.user_service import UsersService
from src.app.core.database import get_db


async def get_tasks_service(
    db: AsyncSession = Depends(get_db)
) -> TasksService:
    """ Возвращает экземпляр сервиса задач. """
    return TasksService(TasksRepository(db))


async def get_users_service(
    db: AsyncSession = Depends(get_db)
) -> UsersService:
    """ Возвращает экземпляр сервиса пользователя """
    return UsersService(UsersRepository(db))
