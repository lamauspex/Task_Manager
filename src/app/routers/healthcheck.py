
""" Назначение: Проверка состояния сервиса """


from fastapi import APIRouter, Response
from datetime import datetime

router = APIRouter(prefix="/healthcheck", tags=["Сheck"])


@router.get("/", summary="Проверка работоспособности сервиса")
async def health_check(response: Response):
    """
    Возвращает статус OK и текущую временную отметку UTC.

    """
    current_time = datetime.utcnow().isoformat()
    return {"status": "OK", "timestamp": current_time}
