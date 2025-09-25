
""" Назначение: Интеграционные исключения """


from src.app.exceptions.base import AppBaseException


class ExternalServiceUnavailable(AppBaseException):
    """Внешний сервис временно недоступен."""

    def __init__(self):
        super().__init__(
            status_code=503,
            detail="Подключённый внешний сервис временно недоступен."
        )
