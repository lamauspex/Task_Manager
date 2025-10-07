
""" Назначение: Маршрутизатор аутентификации """

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.config import app_settings
from src.app.core.security import encode_jwt
from src.app.core.utils import get_current_user
from src.app.services.users_services.auth_service import authenticate_user
from src.app.schemas.users_schemas import AuthUserIn
from src.app.core.constants import Token
from src.app.core.database import get_db


# Объект роутера
router = APIRouter(prefix="/users", tags=["User_Authentication"])


# Аутентификация пользователя
@router.post("/token/",
             response_model=Token,
             summary="Аутентификация пользователя")
async def login_for_access_token(
    form_data: AuthUserIn,
    db: AsyncSession = Depends(get_db)
):
    """
    Обрабатывает форму логина и выдаёт JWT-токен
    """
    authenticated_user = await authenticate_user(db, form_data)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials")

    # Формируем нагрузку токена
    jwt_payload = {
        "sub": authenticated_user.email,
        "exp": datetime.now() + timedelta(
            minutes=app_settings.AUTH_JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        "iat": datetime.now()
    }
    token = encode_jwt(jwt_payload)
    return {"access_token": token, "token_type": "bearer"}


# Контроллер для проверки себя
@router.post("/me/")
async def read_users_me(current_user: str = Depends(get_current_user)):
    """
    Возвращает информацию о текущем авторизованном пользователе.
    """
    return current_user
