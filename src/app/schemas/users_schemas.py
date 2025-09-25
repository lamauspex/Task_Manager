
""" Назначение: Схемы Users """

from typing import Optional
from pydantic import ConfigDict, EmailStr, Field

from src.app.core.constants import Role
from src.app.schemas.base import CreateBase, OutputBase, UpdateBase


class UserBase(CreateBase):
    """ Промежуточная модель для общих полей """
    model_config = ConfigDict(strict=True)

    first_name: str = Field(max_length=30, min_length=3,
                            description="Имя")
    last_name: str = Field(max_length=30, min_length=3,
                           description="Фамилия")
    email: EmailStr = Field(description="Адрес электронной почты.")
    role: str = Field(default=Role.USER,
                      description="Роль пользователя")
    active: bool = Field(default=True,
                         description="Активирован ли аккаунт?")


class UserIn(UserBase):
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Пароль пользователя."
    )


class UserCreate(UserBase):
    """Создание пользователя."""
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Пароль пользователя."
    )


class UserUpdate(UpdateBase):
    """Обновление пользователя."""

    first_name: Optional[str] = Field(max_length=30, min_length=3,
                                      description="Имя")
    last_name: Optional[str] = Field(max_length=30, min_length=3,
                                     description="Фамилия")
    email: Optional[EmailStr] = Field(description="Адрес электронной почты.")


class UserOut(OutputBase, UserBase):
    """ Вывод пользователя """
    pass
