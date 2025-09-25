
""" Назначение: Обработка любого зарегистрированного исключения """


from fastapi import Request
from fastapi.responses import JSONResponse
from src.app.exceptions.base import AppBaseException


async def app_exception_handler(
    request: Request,
    exc: AppBaseException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )
