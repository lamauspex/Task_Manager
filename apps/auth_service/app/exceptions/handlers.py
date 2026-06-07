"""FastAPI exception handlers — registered in application.py."""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from backend.src.app.exceptions.base import AppException

logger = logging.getLogger("task_manager.exceptions")


def _error_response(status_code: int, message: str, details: dict | None = None, error_id: str | None = None) -> JSONResponse:
    body = {"error": {"message": message, "details": details or {}}}
    if error_id:
        body["error"]["error_id"] = error_id
    return JSONResponse(status_code=status_code, content=body)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.warning("AppException [%s]: %s", exc.error_id, exc.message)
        return _error_response(exc.status_code, exc.message, exc.details, exc.error_id)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = [{"field": ".".join(str(l) for l in e["loc"]), "msg": e["msg"]} for e in exc.errors()]
        return _error_response(422, "Validation failed", {"errors": errors})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception on %s %s", request.method, request.url)
        return _error_response(500, "Internal server error")
