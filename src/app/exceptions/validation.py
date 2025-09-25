
""" Назначение: Исключение проверки данных """


from src.app.exceptions.base import AppBaseException


class AppInvalidEmailException(AppBaseException):
    """
    Неверный формат электронного письма.
    """
    status_code = 400
    detail = 'Адрес электронной почты имеет неверный формат.'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class AppPasswordTooShortException(AppBaseException):
    """
    Пароль слишком короткий.
    """
    status_code = 400
    detail = 'Пароль слишком короткий.'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
