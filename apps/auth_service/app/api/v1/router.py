"""
Главный роутер для API версии 1.

Объединяет все endpoint роутеры в один главный роутер.
Используется для версионирования API (v1, v2, etc.).
"""


from fastapi import APIRouter

from backend.src.app.api.v1.endpoints.auth import router as auth_router
from backend.src.app.api.v1.endpoints.users import router as users_router
from backend.src.app.api.v1.endpoints.tasks import router as tasks_router
from backend.src.app.api.v1.endpoints.health import router as health_router


# Создаём главный роутер с префиксом /api/v1
api_v1_router = APIRouter(prefix="/api/v1")
# Роутер аутентификации
api_v1_router.include_router(auth_router)
# Роутер пользователей
api_v1_router.include_router(users_router)
# Роутер задач
api_v1_router.include_router(tasks_router)
# Роутер health checks
api_v1_router.include_router(health_router)
