
""" Назначение: Настройки конфигурации """


from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path='.env')


class AppSettings(BaseSettings):

    # Конфигурация электронной почты
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str

    # Настройки базы данных
    DATABASE_URL: str

    # Настройки JWT-аутентификации
    AUTH_JWT_PRIVATE_KEY_PATH: Path
    AUTH_JWT_PUBLIC_KEY_PATH: Path
    AUTH_JWT_ALGORITHM: str
    AUTH_JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Добавляем общие настройки приложения
    APP_NAME: str
    VERSION: str
    DOCS_URL: str
    OPENAPI_URL: str
    ROOT_PATH: str
    ORIGINS: list[str]

    # Допустимые домены для CORS
    CORS_ALLOW_CREDENTIALS: bool
    CORS_ALLOW_METHODS: list[str]
    CORS_ALLOW_HEADERS: list[str]

    # Дополнительные настройки для FastAPI
    FASTAPI_TITLE: str
    FASTAPI_VERSION: str
    FASTAPI_DOCS_URL: str
    FASTAPI_OPENAPI_URL: str
    FASTAPI_ROOT_PATH: str
    FASTAPI_SERVERS: list
    FASTAPI_CONTACT_NAME: str
    FASTAPI_CONTACT_EMAIL: str
    FASTAPI_LICENSE_NAME: str
    FASTAPI_LICENSE_URL: str

    # Определение FASETAPI_KWARGS в AppSettings
    @property
    def FASTAPI_KWARGS(self):
        return {
            "title": self.FASTAPI_TITLE,
            "version": self.FASTAPI_VERSION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "root_path": self.ROOT_PATH,
            "servers": self.FASTAPI_SERVERS,
            "contact": {
                "name": self.FASTAPI_CONTACT_NAME,
                "email": self.FASTAPI_CONTACT_EMAIL
            },
            "license_info": {
                "name": self.FASTAPI_LICENSE_NAME,
                "url": self.FASTAPI_LICENSE_URL
            }
        }

    class Config(SettingsConfigDict):
        env_file = ".env"


app_settings = AppSettings()
