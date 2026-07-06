""" """


from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    Схема ответа для health check.

    Attributes:
        status: Статус сервиса (ok/error).
        version: Версия приложения.
        environment: Среда выполнения (dev/prod).
    """
    status: str = Field(
        ...,
        description=" Статус работоспособности"
        )
    version: str = Field(
        ..., 
        description="Версия приложения"
        )
    environment: str = Field(
        ..., 
        description="Среда выполнения"
        )
