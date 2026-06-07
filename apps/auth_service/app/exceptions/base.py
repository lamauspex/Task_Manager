"""Base application exception."""

import uuid


class AppException(Exception):
    """All domain exceptions inherit from this."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: dict | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.error_id = str(uuid.uuid4())
