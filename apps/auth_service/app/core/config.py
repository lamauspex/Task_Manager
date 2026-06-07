"""
Модуль конфигурации приложения через pydantic-settings.

Централизованное хранение всех настроек приложения.
Загружает переменные окружения из .env файла.
"""

# Импорты для работы с путями
from pathlib import Path
# Импорты для валидации полей Pydantic
from pydantic import field_validator
# Импорты базовых настроек Pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict


# Базовая директория проекта (4 уровня вверх от этого файла)
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class AppSettings(BaseSettings):
    """
    Класс основных настроек приложения.

    Наследуется от BaseSettings для автоматической загрузки из env.
    """
    # Конфигурация модели: откуда загружать настройки
    model_config = SettingsConfigDict(
        env_file=".env",  # Файл с переменными окружения
        env_file_encoding="utf-8",  # Кодировка файла
        case_sensitive=True,  # Чувствительность к регистру имён
        extra="ignore",  # Игнорировать неизвестные поля
    )

    # ── App (Настройки приложения) ───────────────────────────────────────────
    APP_NAME: str = "Task Manager Pro"  # Название приложения
    VERSION: str = "2.0.0"  # Версия приложения
    DEBUG: bool = False  # Режим отладки (True для разработки)
    ENVIRONMENT: str = "production"  # Среда выполнения (dev/staging/prod)

    # ── API (Настройки API) ──────────────────────────────────────────────────
    API_V1_PREFIX: str = "/api/v1"  # Префикс для API версии 1
    DOCS_URL: str = "/docs"  # URL для Swagger документации
    OPENAPI_URL: str = "/openapi.json"  # URL для OpenAPI спецификации

    # ── CORS (Настройки Cross-Origin) ────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:3000",
                               "http://localhost:5173"]  # Разрешённые origin
    CORS_ALLOW_CREDENTIALS: bool = True  # Разрешить передачу credentials

    # ── Database (Настройки БД) ──────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./task_manager.db"  # URL подключения к БД

    # ── JWT (Настройки JWT токенов) ──────────────────────────────────────────
    JWT_PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / \
        "private.pem"  # Путь к приватному ключу
    JWT_PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / \
        "public.pem"  # Путь к публичному ключу
    JWT_ALGORITHM: str = "RS256"  # Алгоритм подписи JWT
    # Время жизни access токена (минуты)
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # Время жизни refresh токена (дни)

    # ── Redis (Настройки Redis) ──────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"  # URL подключения к Redis

    # ── Email (Настройки почты) ──────────────────────────────────────────────
    EMAIL_HOST: str = "smtp.gmail.com"  # SMTP сервер
    EMAIL_PORT: int = 587  # SMTP порт
    EMAIL_USER: str = ""  # Пользователь SMTP
    EMAIL_PASSWORD: str = ""  # Пароль SMTP
    EMAIL_FROM_NAME: str = "Task Manager Pro"  # Имя отправителя
    EMAIL_ENABLED: bool = False  # Включена ли отправка email

    # ── Google Calendar (Интеграция с Google) ────────────────────────────────
    GOOGLE_CLIENT_ID: str = ""  # Client ID для Google OAuth
    GOOGLE_CLIENT_SECRET: str = ""  # Client Secret для Google OAuth
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/integrations/google/callback"  # Redirect URI

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def validate_db_url(cls, v: str) -> str:
        """
        Валидатор URL базы данных.

        Гарантирует использование async драйверов для SQLAlchemy.

        Args:
            v: Исходный URL базы данных.

        Returns:
            str: URL с async драйвером.
        """
        # Обеспечиваем использование асинхронного драйвера
        # Заменяем postgresql:// на postgresql+asyncpg://
        if v.startswith("postgresql://"):
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        # Заменяем sqlite:/// на sqlite+aiosqlite:///
        if v.startswith("sqlite:///"):
            return v.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
        return v

    @property
    def fastapi_kwargs(self) -> dict:
        """
        Словарь параметров для инициализации FastAPI.

        Returns:
            dict: Параметры для FastAPI(title, version, docs_url, etc.)
        """
        return {
            "title": self.APP_NAME,  # Название для OpenAPI
            "version": self.VERSION,  # Версия для OpenAPI
            "docs_url": self.DOCS_URL if self.DEBUG else None,  # Docs только в debug
            "openapi_url": self.OPENAPI_URL if self.DEBUG else None,  # OpenAPI только в debug
            "contact": {"name": "Task Manager Team"},  # Контактная информация
        }


# Глобальный экземпляр настроек (singleton)
settings = AppSettings()
