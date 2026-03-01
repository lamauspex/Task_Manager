"""Точка входа в приложение"""

import uvicorn

from certs.generate_jwt_keys import generate_jwt_keys
from src.application import create_app


# Генерация JWT ключей при первом запуске
generate_jwt_keys()

# Создание приложения
app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
