
""" Назначение: Базовый класс исключений """

from fastapi import HTTPException
from typing import Any, Dict, List, Optional


class AppBaseException(HTTPException):
    def __init__(
        self,
        *,
        status_code: int,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        error_id: Optional[int] = None,
        meta: Optional[List[str]] = None
    ) -> None:
        if not isinstance(details, dict):
            details = {}
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "details": details,
                "error_id": error_id,
                "meta": meta
            }
        )
