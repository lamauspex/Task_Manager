

from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.app.exceptions.base import AppBaseException

app = FastAPI()


@app.exception_handler(AppBaseException)
async def app_base_exception_handler(request: Request, exc: AppBaseException):
    """
    Универсальная обработка исключений уровня приложения.
    Передаёт клиенту объект с подробной информацией об ошибке.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    """
    Обработчик исключений валидации запросов.
    Формирует список ошибок в понятном формате.
    """
    errors = [
        {
            "field": ".".join(map(str, err["loc"])),
            "message": err["msg"],
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"errors": errors},
    )
