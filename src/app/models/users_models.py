""" Назначение: Модели пользователей """


from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import String, Boolean, Enum

from src.app.core.constants import Role
from src.app.core.database import Base
from src.app.models.base import BaseModel


class User(Base, BaseModel):
    """ Таблица Users """

    first_name: Mapped[str] = mapped_column(
        String(length=50),
        nullable=False,
        comment='Имя'
    )

    last_name: Mapped[str] = mapped_column(
        String(length=30),
        nullable=False,
        comment='Фамилия'
    )

    email: Mapped[str] = mapped_column(
        String(length=255),
        unique=True,
        index=True,
        nullable=False,
        comment='Email'
    )

    password_hash: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False,
        comment='Хэш пароля'
    )

    role: Mapped[str] = mapped_column(
        String(length=10),
        default=Role.USER.value,
        nullable=False,
        comment='Роль пользователя в системе'
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default='TRUE',
        comment='Активность пользователя'
    )

    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if len(first_name) > 50:
            raise ValueError(
                f"First name cannot exceed 50 characters, got {len(first_name)}")
        return first_name

    @validates('last_name')
    def validate_last_name(self, key, last_name):
        if len(last_name) > 30:
            raise ValueError(
                f"Last name cannot exceed 30 characters, got {len(last_name)}")
        return last_name

    @validates('email')
    def validate_email(self, key, email):
        if len(email) > 255:
            raise ValueError(
                f"Email cannot exceed 255 characters, got {len(email)}")
        return email

    @validates('role')
    def validate_role(self, key, role):
        # Проверяем, что роль соответствует одному из допустимых значений
        valid_roles = [r.value for r in Role]
        if role not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}, got {role}")
        return role

    @property
    def full_name(self) -> str:
        """Вычисляемое свойство для полного имени"""
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        """Строковое представление для отладки"""
        return f"User(id={self.id}, name={self.full_name}, email={self.email})"
