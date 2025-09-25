
""" Назначение: Исключения взаимодействия с базой данных """


from src.app.exceptions.base import AppBaseException


class DatabaseConnectionError(AppBaseException):
    """Ошибка подключения к базе данных."""

    def __init__(self):
        super().__init__(
            status_code=500,
            detail="Ошибка соединения с базой данных."
        )


class AppDatabaseIntegrityViolation(AppBaseException):
    """Нарушение целостности данных в базе данных."""

    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Данные нарушают ограничения целостности базы данных."
        )
