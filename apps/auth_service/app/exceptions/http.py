"""HTTP-mapped application exceptions."""

from backend.src.app.exceptions.base import AppException


class NotFoundError(AppException):
    def __init__(self, resource: str, resource_id: str | None = None) -> None:
        msg = f"{resource} not found"
        if resource_id:
            msg += f": {resource_id}"
        super().__init__(msg, status_code=404)


class ConflictError(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=409)


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(message, status_code=401)


class ForbiddenError(AppException):
    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(message, status_code=403)


class UnprocessableError(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=422)
