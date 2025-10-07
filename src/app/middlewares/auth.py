
""" Назначение: Авторизационная middleware """


from fastapi import FastAPI, Request, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from datetime import datetime

from src.app.core.config import app_settings


# Класс-обёртка вокруг middleware
class AuthenticationMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app
        self.bearer_scheme = HTTPBearer(auto_error=False)

    async def __call__(self, request: Request, call_next):
        # Пробуем извлечь токен из запроса
        authorization_header = request.headers.get("Authorization")
        if authorization_header:
            scheme, _, credentials = authorization_header.partition(" ")
            if scheme.lower() == "bearer":
                # Попробуем распарсить токен
                try:
                    payload = jwt.decode(
                        credentials,
                        app_settings.AUTH_JWT_PUBLIC_KEY_PATH.read_text(),
                        algorithms=[app_settings.AUTH_JWT_ALGORITHM]
                    )

                    # Проверьте срок годности токена
                    expiration_time = datetime.fromtimestamp(
                        payload.get("exp"))
                    if expiration_time < datetime.now():
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Expired token"
                        )

                    # Сохраняем payload в state запроса
                    request.state.user = payload

                except JWTError:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token"
                    )

        else:
            # Если нет авторизации, пропускаем дальше
            pass

        # Переходим к следующему обработчику
        response = await call_next(request)
        return response


# Регистрация middleware в приложении
def include_auth_middleware(app: FastAPI):
    app.middleware("http")(AuthenticationMiddleware(app))
