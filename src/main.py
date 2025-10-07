
""" Назначение: Главный файл """


import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from src.app.core.config import app_settings
from src.app.analytics.home import home_page
from src.app.routers import register_routes
from src.app.middlewares.logging import LoggingSettings
from src.app.middlewares.auth import include_auth_middleware

# Устанавливаем логирование
logger = LoggingSettings.setup_logging()

# Основной инстанс FastAPI
app = FastAPI(**app_settings.FASTAPI_KWARGS)

# Средства защиты от межсайтового взаимодействия (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.ORIGINS,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"]
)

# Роут для главной страницы
app.get("/", response_class=HTMLResponse)(home_page)

# Регистрация маршрутов
register_routes(app)
include_auth_middleware(app)


@app.on_event("startup")
async def startup():
    """Настройка подключения к базе данных"""
    from src.app.core.database import init_database
    await init_database()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
