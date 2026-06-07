"""
Фабрики зависимостей сервисов — подключаются через FastAPI Depends.

Централизованное создание сервисов и репозиториев для dependency injection.
"""

# Импорты для аннотаций типов
from typing import Annotated
# Импорты FastAPI для зависимостей
from fastapi import Depends
# Импорты SQLAlchemy для сессий
from sqlalchemy.ext.asyncio import AsyncSession

# Импорты функции получения сессии БД
from backend.src.app.core.database import get_session  # Dependency для сессии
# Импорты репозиториев
# Репозиторий пользователей
from backend.src.app.repositories.user import UserRepository
from backend.src.app.repositories.task import TaskRepository  # Репозиторий задач
# Импорты сервисов
from backend.src.app.services.auth.service import AuthService  # Сервис аутентификации
from backend.src.app.services.tasks.service import TaskService  # Сервис задач
# Сервис уведомлений
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
    # Создаём репозиторий с сессией БД
    return UserRepository(session)


def get_task_repository(session: AsyncSession = Depends(get_session)) -> TaskRepository:
    """
    Фабрика TaskRepository для dependency injection.

    Args:
        session: Сессия БД (внедряется автоматически).

    Returns:
        TaskRepository: Экземпляр репозитория задач.
    """
    # Создаём репозиторий с сессией БД
    return TaskRepository(session)


# ── Service factories (Фабрики сервисов) ─────────────────────────────────────

def get_notification_service() -> NotificationService:
    """
    Фабрика NotificationService для dependency injection.

    Returns:
        NotificationService: Экземпляр сервиса уведомлений.
    """
    # Создаём сервис уведомлений (без зависимостей)
    return NotificationService()


def get_auth_service(
    user_repo: UserRepository = Depends(
        get_user_repository),  # Внедряем репозиторий
) -> AuthService:
    """
    Фабрика AuthService для dependency injection.

    Args:
        user_repo: Репозиторий пользователей (внедряется через Depends).

    Returns:
        AuthService: Экземпляр сервиса аутентификации.
    """
    # Создаём сервис аутентификации с репозиторием
    return AuthService(user_repo)


def get_task_service(
    task_repo: TaskRepository = Depends(
        get_task_repository),  # Внедряем репозиторий задач
    # Внедряем репозиторий пользователей
    user_repo: UserRepository = Depends(get_user_repository),
    notifications: NotificationService = Depends(
        get_notification_service),  # Внедряем сервис уведомлений
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
