
""" Назначение: HTTP-исключения """


from src.app.exceptions.base import AppBaseException


class AppHttpNotFound(AppBaseException):
    """
    Ресурс не найден (HTTP 404).
    """

    def __init__(self, resource_name: str):
        super().__init__(
            status_code=404,
            detail=f'{resource_name.capitalize()} не найден.'
        )


class AppHttpBadRequest(AppBaseException):
    """
    Некорректный запрос (HTTP 400).
    """

    def __init__(self, reason: str):
        super().__init__(
            status_code=400,
            detail=f'Некорректный запрос: {reason}.'
        )
