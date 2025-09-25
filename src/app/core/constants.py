
""" Назначение: Файл для общих констант и классов-перечислений """

from enum import StrEnum
from pydantic import BaseModel


# Статусы задач
class TaskStatus(StrEnum):
    CREATED = 'CREATED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'


# Роли пользователей
class Role(StrEnum):
    USER = 'USER'
    ADMIN = 'ADMIN'


# Классы схем токенов
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str
    exp: float
    iat: float
