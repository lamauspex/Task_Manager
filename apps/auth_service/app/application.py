"""
Фабрика приложения FastAPI.

Единственная ответственность: сборка FastAPI приложения.
Никакой бизнес-логики здесь — только подключение компонентов (wiring).
"""

# Импорты для контекстного менеджера жизненного цикла приложения
from contextlib import asynccontextmanager
# Импорты FastAPI и middleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Импорты настроек и конфигурации
from backend.src.app.core.config import settings
# Импорты базы данных (движок и базовая модель)
from backend.src.app.core.database import engine, Base
# Импорты логирования
from backend.src.app.core.logging import configure_logging
# Импорты обработчиков исключений
from backend.src.app.exceptions.handlers import register_exception_handlers
# Импорты middleware логирования запросов
from backend.src.app.middlewares.logging import RequestLoggingMiddleware
# Импорты главного роутера API v1
from backend.src.app.api.v1.router import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Менеджер жизненного цикла приложения (старт/остановка).

    Вызывается при запуске и завершении работы приложения.
    """
    # Настраиваем логирование при старте
    configure_logging()
    # ПРИМЕЧАНИЕ: В продакшене используйте Alembic миграции вместо create_all.
    # create_all оставлен только для удобства разработки.
    # Создаём все таблицы БД если режим отладки включён
    if settings.DEBUG:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    # Возвращаем управление приложению (точка работы)
    yield
    # Освобождаем ресурсы базы данных при остановке
    await engine.dispose()


def create_app() -> FastAPI:
    """
    Функция-фабрика для создания экземпляра FastAPI приложения.

    Returns:
        FastAPI: Настроенное приложение со всеми middleware и роутами.
    """
    # Создаём приложение с менеджером жизненного цикла и настройками
    app = FastAPI(lifespan=lifespan, **settings.fastapi_kwargs)

    # ── CORS (Cross-Origin Resource Sharing) ──────────────────────────────────
    # Разрешаем запросы с указанных.origin (для frontend)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,  # Список разрешённых origin
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,  # Разрешить cookies
        allow_methods=["*"],  # Разрешить все HTTP методы
        allow_headers=["*"],  # Разрешить все заголовки
    )

    # ── Custom middleware (Пользовательские middleware) ───────────────────────
    # Добавляем middleware для логирования всех запросов
    app.add_middleware(RequestLoggingMiddleware)

    # ── Exception handlers (Обработчики исключений) ───────────────────────────
    # Регистрируем глобальные обработчики исключений
    register_exception_handlers(app)

    # ── Routers (Роутеры/Endpoints) ───────────────────────────────────────────
    # Подключаем главный роутер API версии 1
    app.include_router(api_v1_router)

    return app
