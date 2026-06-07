"""
ORM модель пользователя.

Определяет таблицу users в базе данных.
Наследуется от BaseModel (id, created_at, updated_at).
"""

# Импорты для генерации UUID
import uuid
# Импорты типов колонок SQLAlchemy
from sqlalchemy import Boolean, String
# Импорты для типизации ORM
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

# Импорты констант ролей
from backend.src.app.core.constants import Role  # USER, ADMIN, etc.
# Импорты базовой модели
from backend.src.app.models.base import BaseModel  # Базовый класс с id, timestamps


class User(BaseModel):
    """
    Модель пользователя в базе данных.

    Представляет таблицу users с полями аутентификации и профиля.
    """
    # Имя таблицы в базе данных
    __tablename__ = "users"

    # Поле: Имя пользователя (до 50 символов)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    # Поле: Фамилия пользователя (до 50 символов)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    # Поле: Email (уникальный, индексированный, обязательный)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    # Поле: Хеш пароля (до 255 символов, обязательный)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    # Поле: Роль пользователя (USER, ADMIN, etc.)
    role: Mapped[str] = mapped_column(
        String(10), default=Role.USER, nullable=False
    )
    # Поле: Активен ли пользователь (по умолчанию True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="TRUE"
    )

    # ── Relationships (Связи с другими таблицами) ─────────────────────────────

    # Связь: Задачи назначенные пользователю (Many-to-One)
    assigned_tasks: Mapped[list["Task"]] = relationship(  # type: ignore[name-defined]
        "Task",  # Имя связанной модели
        foreign_keys="Task.assigned_to_id",  # Внешний ключ
        back_populates="assigned_to",  # Обратная связь
        lazy="selectin",  # Стратегия загрузки (eager loading)
    )
    # Связь: Задачи выполненные пользователем (Many-to-One)
    completed_tasks: Mapped[list["Task"]] = relationship(  # type: ignore[name-defined]
        "Task",  # Имя связанной модели
        foreign_keys="Task.completed_by_id",  # Внешний ключ
        back_populates="completed_by",  # Обратная связь
        lazy="selectin",  # Стратегия загрузки
    )
    # Связь: Refresh токены пользователя (One-to-Many, каскадное удаление)
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(  # type: ignore[name-defined]
        "RefreshToken",  # Имя связанной модели
        back_populates="user",  # Обратная связь
        cascade="all, delete-orphan",  # Каскад: удалить токены при удалении пользователя
    )

    @validates("email")
    def _lower_email(self, _key: str, value: str) -> str:
        """
        Валидатор email: приведение к нижнему регистру.

        Args:
            _key: Имя поля (email).
            value: Значение поля.

        Returns:
            str: Email в нижнем регистре без пробелов.
        """
        # Приводим email к нижнему регистру и убираем пробелы
        return value.lower().strip()

    @validates("role")
    def _validate_role(self, _key: str, value: str) -> str:
        """
        Валидатор роли: проверка на допустимое значение.

        Args:
            _key: Имя поля (role).
            value: Значение поля.

        Returns:
            str: Проверенное значение роли.

        Raises:
            ValueError: Если роль недопустима.
        """
        # Набор допустимых ролей из констант
        valid = {r.value for r in Role}
        # Проверяем наличие роли в допустимых
        if value not in valid:
            raise ValueError(
                f"Недопустимая роль '{value}'. Допустимы: {valid}")
        return value

    @property
    def full_name(self) -> str:
        """
        Полное имя пользователя.

        Returns:
            str: Фамилия и имя вместе.
        """
        # Формируем полное имя
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        """
        Строковое представление пользователя.

        Returns:
            str: Строка с email и ролью.
        """
        return f"User({self.email!r}, role={self.role})"
