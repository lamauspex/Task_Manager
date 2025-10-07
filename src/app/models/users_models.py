
""" Назначение: Модели пользователей """


from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Enum

from src.app.core.constants import Role
from src.app.core.database import Base
from src.app.models.base import BaseModel


class User(Base, BaseModel):
    """ Таблица Users """

    first_name: Mapped[str] = mapped_column(String(length=30))
    last_name: Mapped[str] = mapped_column(String(length=30))
    email: Mapped[str] = mapped_column(
        String(length=100),
        unique=True,
        index=True
    )
    password_hash: Mapped[str] = mapped_column(
        String(length=128),
        nullable=False
    )

    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.USER)
    active: Mapped[bool] = mapped_column(Boolean)
