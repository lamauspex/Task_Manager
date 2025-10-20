
""" Назначение: Схемы Users """

from typing import Optional
from pydantic import ConfigDict, EmailStr, Field, BaseModel, computed_field

from src.app.core.constants import Role
from src.app.schemas.base import CreateBase, OutputBase, UpdateBase


class UserBase(CreateBase):
    """ Промежуточная модель для общих полей """
    model_config = ConfigDict(
        strict=True,
        str_strip_whitespace=True,
        str_to_lower=True,
        extra='forbid')

    first_name: str = Field(
        max_length=30,
        min_length=2,
        description="Имя",
        examples=["Кирилл", "Полина"]
    )
    last_name: str = Field(
        max_length=30,
        min_length=2,
        description="Фамилия",
        examples=["Иванов", "Сидоров"]
    )
    email: EmailStr = Field(
        description="Адрес электронной почты.",
        examples=["test@example.com"]
    )
    role: str = Field(
        default=Role.USER,
        description="Роль пользователя"
    )
    active: bool = Field(
        default=True,
        description="Активирован ли аккаунт?"
    )


class UserIn(UserBase):
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Пароль пользователя."
    )


class AuthUserIn(BaseModel):
    """ Модель для входа в систему """
    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_to_lower=True,
        extra='forbid'
    )

    email: EmailStr = Field(
        description="Адрес электронной почты",
        examples=["user@example.com"]
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Пароль пользователя",
        examples=["SecurePassword123!"]
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
    model_config = ConfigDict(extra='forbid')

    first_name: Optional[str] = Field(
        max_length=30,
        min_length=3,
        description="Имя"
    )
    last_name: Optional[str] = Field(
        max_length=30,
        min_length=3,
        description="Фамилия"
    )
    email: Optional[EmailStr] = Field(
        description="Адрес электронной почты."
    )

    model_config = ConfigDict(extra='forbid')


class UserOut(OutputBase, UserBase):
    """ Вывод пользователя """
    model_config = ConfigDict(extra='forbid')

    @computed_field
    @property
    def full_name(self) -> str:
        """Вычисляемое поле для полного имени"""
        return f"{self.first_name} {self.last_name}"


class UserLoginResponse(BaseModel):
    """Схема ответа при успешном входе"""
    access_token: str = Field(
        description="JWT токен доступа"
    )
    token_type: str = Field(
        default="bearer",
        description="Тип токена"
    )
    user: UserOut = Field(
        description="Данные пользователя"
    )


class UserProfileResponse(UserOut):
    """Расширенная схема для профиля пользователя"""
    pass
