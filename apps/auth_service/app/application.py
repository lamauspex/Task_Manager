"""
Фабрика приложения FastAPI.

Единственная ответственность: сборка FastAPI приложения.
Никакой бизнес-логики здесь — только подключение компонентов (wiring).
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.app.core.config import settings
from backend.src.app.core.database import engine, Base
from backend.src.app.core.logging import configure_logging
from backend.src.app.exceptions.handlers import register_exception_handlers
from backend.src.app.middlewares.logging import RequestLoggingMiddleware
from backend.src.app.api.v1.router import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Менеджер жизненного цикла приложения (старт/остановка).

    Вызывается при запуске и завершении работы приложения.
    """
    configure_logging()

    if settings.DEBUG:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    """
    Функция-фабрика для создания экземпляра FastAPI приложения.

    Returns:
        FastAPI: Настроенное приложение со всеми middleware и роутами.
    """

    app = FastAPI(lifespan=lifespan, **settings.fastapi_kwargs)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS, 
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS, 
        allow_methods=["*"], 
        allow_headers=["*"],
    )


    app.add_middleware(RequestLoggingMiddleware)

    register_exception_handlers(app)

    app.include_router(api_v1_router)

    return app
