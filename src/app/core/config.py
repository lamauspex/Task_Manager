""" Назначение: Настройки конфигурации """


from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path='.env')


class AppSettings(BaseSettings):
    DATABASE_URL: str
    AUTH_JWT_PRIVATE_KEY_PATH: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    AUTH_JWT_PUBLIC_KEY_PATH: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    AUTH_JWT_ALGORITHM: str = 'RS256'
    AUTH_JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    # Добавляем общие настройки приложения
    APP_NAME: str = "Task Manager API"
    VERSION: str = "0.1.0"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    ROOT_PATH: str = "/api/v1"
    ORIGINS: list[str] = ["http://localhost:8080"]

    # Допустимые домены для CORS
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = [""]
    CORS_ALLOW_HEADERS: list[str] = [""]

    # Дополнительные настройки для FastAPI
    FASTAPI_TITLE: str = "Task Manager API"
    FASTAPI_VERSION: str = "0.1.0"
    FASTAPI_DOCS_URL: str = "/docs"
    FASTAPI_OPENAPI_URL: str = "/openapi.json"
    FASTAPI_ROOT_PATH: str = "/api/v1"
    FASTAPI_SERVERS: list = []
    FASTAPI_CONTACT_NAME: str = "Кирилл Резник"
    FASTAPI_CONTACT_EMAIL: str = "lamauspex@yandex.ru"
    FASTAPI_LICENSE_NAME: str = "MIT License"
    FASTAPI_LICENSE_URL: str = "https://opensource.org/licenses/MIT"

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
