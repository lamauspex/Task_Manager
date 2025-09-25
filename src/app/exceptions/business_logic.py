
""" Назначение: Исключения бизнес-логики """


from src.app.core.constants import Role
from src.app.exceptions.base import AppBaseException


class InvalidUserRole(AppBaseException):
    """ Недостаточно прав пользователя """

    def __init__(self):
        super().__init__(
            status_code=403,
            message="Недостаточно прав пользователя",
            details={"role": Role.USER},
            error_id=1001
        )


class IncorrectPassword(AppBaseException):
    """Неправильный пароль для входа или изменения пароля."""

    def __init__(self):
        super().__init__(
            status_code=401,
            message="Неверный пароль.",
            error_id=1002
        )
