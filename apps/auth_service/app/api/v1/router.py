"""
Главный роутер для API версии 1.

Объединяет все endpoint роутеры в один главный роутер.
Используется для версионирования API (v1, v2, etc.).
"""

# Импорты APIRouter из FastAPI
from fastapi import APIRouter

# Импорты роутеров для каждого модуля
# Роутер аутентификации
from backend.src.app.api.v1.endpoints.auth import router as auth_router
# Роутер пользователей
from backend.src.app.api.v1.endpoints.users import router as users_router
from backend.src.app.api.v1.endpoints.tasks import router as tasks_router  # Роутер задач
# Роутер health checks
from backend.src.app.api.v1.endpoints.health import router as health_router

# Создаём главный роутер с префиксом /api/v1
api_v1_router = APIRouter(prefix="/api/v1")
# Подключаем роутер аутентификации
api_v1_router.include_router(auth_router)
# Подключаем роутер пользователей
api_v1_router.include_router(users_router)
# Подключаем роутер задач
api_v1_router.include_router(tasks_router)
# Подключаем роутер health checks
api_v1_router.include_router(health_router)
