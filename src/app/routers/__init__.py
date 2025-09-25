

from fastapi import APIRouter
from src.app.routers.users_routes.users_router import router as users_router
from src.app.routers.tasks_routes.tasks_router import router as tasks_router
from src.app.routers.healthcheck import router as healthcheck_router


router = APIRouter()


def register_routes(app):
    """Регистрирует все маршруты приложения."""
    app.include_router(router)
    app.include_router(users_router)
    app.include_router(tasks_router)
    app.include_router(healthcheck_router)
