"""
Endpoints для проверки работоспособности сервиса (Health Checks).

Используется мониторингом и load balancer'ами для проверки статуса сервиса.
"""

# Импорты FastAPI для роутеров
from fastapi import APIRouter
# Импорты Pydantic для схем ответа
from pydantic import BaseModel
# Импорты настроек приложения
from backend.src.app.core.config import settings

# Создаём роутер с тегом Health
router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """
    Схема ответа для health check.

    Attributes:
        status: Статус сервиса (ok/error).
        version: Версия приложения.
        environment: Среда выполнения (dev/prod).
    """
    status: str  # Статус работоспособности
    version: str  # Версия приложения
    environment: str  # Среда выполнения


@router.get(
    "/health",  # GET /api/v1/health
    response_model=HealthResponse,  # Модель ответа
    summary="Service health check"  # Краткое описание для Swagger
)
async def health_check() -> HealthResponse:
    """
    Проверка работоспособности сервиса.

    Returns:
        HealthResponse: Статус, версия и среда приложения.
    """
    # Возвращаем ответ со статусом сервиса
    return HealthResponse(
        status="ok",  # Статус: всё работает
        version=settings.VERSION,  # Версия из настроек
        environment=settings.ENVIRONMENT,  # Среда из настроек
    )
