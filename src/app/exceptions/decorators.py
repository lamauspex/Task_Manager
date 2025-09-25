

from functools import wraps
from typing import Awaitable, Callable, TypeVar, ParamSpec
from fastapi import Response
from starlette.datastructures import Headers

from src.app.exceptions.base import AppBaseException
from src.app.middlewares.logging import LoggingSettings

logger = LoggingSettings.setup_logging()

P = ParamSpec('P')
R = TypeVar('R', bound=Awaitable)


def exception_handler(
    handler_func: Callable[P, Awaitable[R]]
) -> Callable[P, Awaitable[R]]:
    @wraps(handler_func)
    async def wrapped_handler(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            response = await handler_func(*args, **kwargs)
            return response
        except AppBaseException as err:
            # Регистрация ошибки в логах
            logger.error(
                f"Application error occurred: {err.detail}, traceback={err.__traceback__}")

            # Формируем ответ с уникальными метаданными
            headers = Headers({
                "X-Error-ID": f"{err.error_id}",
                "Content-Type": "application/json"
            })

            return Response(
                content={
                    'message': err.message,
                    'details': err.details
                },
                status_code=err.status_code,
                headers=headers
            )

        except Exception as general_err:
            # Внутренняя ошибка сервера, регистрация полного stacktrace
            logger.critical(
                f"Unexpected server error: {general_err}, traceback={general_err.__traceback__}")

            return Response(content="Internal Server Error", status_code=500)

    return wrapped_handler
