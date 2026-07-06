"""
Endpoints для проверки работоспособности сервиса (Health Checks).

Используется мониторингом и load balancer'ами для проверки статуса сервиса.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.src.app.core.config import settings


router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """
    Схема ответа для health check.

    Attributes:
        status: Статус сервиса (ok/error).
        version: Версия приложения.
        environment: Среда выполнения (dev/prod).
    """
    status: str       # Статус работоспособности
    version: str      # Версия приложения
    environment: str  # Среда выполнения


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service health check"
)
async def health_check() -> HealthResponse:
    """
    Проверка работоспособности сервиса.

    Returns:
        HealthResponse: Статус, версия и среда приложения.
    """
    # Возвращаем ответ со статусом сервиса
    return HealthResponse(
        status="ok",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
    )
