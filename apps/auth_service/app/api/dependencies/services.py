"""
Фабрики зависимостей сервисов — подключаются через FastAPI Depends.

Централизованное создание сервисов и репозиториев для dependency injection.
"""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.app.core.database import get_session
from backend.src.app.repositories.user import UserRepository
from backend.src.app.repositories.task import TaskRepository
from backend.src.app.services.auth.service import AuthService
from backend.src.app.services.tasks.service import TaskService
from backend.src.app.services.notifications.service import NotificationService


# ── Repository factories (Фабрики репозиториев) ──────────────────────────────

def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    """
    Фабрика UserRepository для dependency injection.

    Args:
        session: Сессия БД (внедряется автоматически через Depends).

    Returns:
        UserRepository: Экземпляр репозитория пользователей.
    """
    return UserRepository(session)


def get_task_repository(session: AsyncSession = Depends(get_session)) -> TaskRepository:
    """
    Фабрика TaskRepository для dependency injection.

    Args:
        session: Сессия БД (внедряется автоматически).

    Returns:
        TaskRepository: Экземпляр репозитория задач.
    """
    return TaskRepository(session)


# ── Service factories (Фабрики сервисов) ─────────────────────────────────────

def get_notification_service() -> NotificationService:
    """
    Фабрика NotificationService для dependency injection.

    Returns:
        NotificationService: Экземпляр сервиса уведомлений.
    """

    return NotificationService()


def get_auth_service(
    user_repo: UserRepository = Depends(
        get_user_repository),
) -> AuthService:
    """
    Фабрика AuthService для dependency injection.

    Args:
        user_repo: Репозиторий пользователей (внедряется через Depends).

    Returns:
        AuthService: Экземпляр сервиса аутентификации.
    """

    return AuthService(user_repo)


def get_task_service(
    task_repo: TaskRepository = Depends(
        get_task_repository),
    user_repo: UserRepository = Depends(get_user_repository),
    notifications: NotificationService = Depends(
        get_notification_service),
) -> TaskService:
    """
    Фабрика TaskService для dependency injection.

    Args:
        task_repo: Репозиторий задач.
        user_repo: Репозиторий пользователей.
        notifications: Сервис уведомлений.

    Returns:
        TaskService: Экземпляр сервиса задач.
    """
    # Создаём сервис задач со всеми зависимостями
    return TaskService(task_repo, user_repo, notifications)
