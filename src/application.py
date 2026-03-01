"""Создание FastAPI приложения"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from src.app.core.config import app_settings
from src.app.analytics.home import home_page
from src.app.routers import register_routes
from src.app.middlewares.logging import LoggingSettings
from src.app.middlewares.auth import include_auth_middleware
from src.app.core.database import init_database


def setup_middleware(app: FastAPI) -> None:
    """Настройка middleware приложения"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.ORIGINS,
        allow_credentials=True,
        allow_methods=[""],
        allow_headers=["*"]
    )


def setup_routes(app: FastAPI) -> None:
    """Настройка маршрутов приложения"""
    app.get("/", response_class=HTMLResponse)(home_page)
    register_routes(app)
    include_auth_middleware(app)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    await init_database()
    yield


def create_app() -> FastAPI:
    """Создание и настройка FastAPI приложения"""
    # Устанавливаем логирование
    LoggingSettings.setup_logging()

    app = FastAPI(
        lifespan=lifespan,
        **app_settings.FASTAPI_KWARGS
    )

    setup_middleware(app)
    setup_routes(app)

    return app
