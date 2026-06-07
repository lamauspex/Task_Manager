"""
Модуль асинхронного движка SQLAlchemy и фабрики сессий.

Настройка подключения к базе данных, создание сессий.
Используется для dependency injection в API endpoints.
"""

# Импорты для асинхронных генераторов
from collections.abc import AsyncGenerator
# Импорты для аннотаций типов
from typing import Annotated

# Импорты FastAPI для зависимостей
from fastapi import Depends
# Импорты SQLAlchemy для асинхронной работы с БД
from sqlalchemy.ext.asyncio import (
    AsyncSession,  # Асинхронная сессия
    async_sessionmaker,  # Фабрика сессий
    create_async_engine,  # Создание асинхронного движка
)
# Импорты базового класса для ORM моделей
from sqlalchemy.orm import DeclarativeBase

# Импорты настроек приложения
from backend.src.app.core.config import settings


# Создание асинхронного движка для подключения к БД
engine = create_async_engine(
    settings.DATABASE_URL,  # URL из настроек
    echo=settings.DEBUG,  # Логирование SQL запросов в debug режиме
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_recycle=3600,  # Пересоздание соединений через 1 час
)

# Фабрика для создания асинхронных сессий
async_session_factory = async_sessionmaker(
    bind=engine,  # Привязка к движку
    class_=AsyncSession,  # Класс сессии
    expire_on_commit=False,  # Не сбрасывать объекты после коммита
    autoflush=False,  # Отключить авто-flush
)


class Base(DeclarativeBase):
    """
    Базовый класс для всех ORM моделей.

    От этого класса наследуются все модели базы данных.
    """
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency: генератор асинхронной DB сессии для FastAPI.

    Создаёт сессию, передаёт её в endpoint, затем фиксирует или откатывает.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy.

    Raises:
        Exception: При ошибке откатывает транзакцию.
    """
    # Создаём сессию через фабрику
    async with async_session_factory() as session:
        try:
            # Передаём сессию в endpoint
            yield session
            # Если всё успешно — коммитим транзакцию
            await session.commit()
        except Exception:
            # При ошибке — откатываем транзакцию
            await session.rollback()
            # Пробрасываем исключение дальше
            raise


# Annotated сокращение для dependency injection в типах
# Использование: session: DBSession в параметрах endpoint
DBSession = Annotated[AsyncSession, Depends(get_session)]
