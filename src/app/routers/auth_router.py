""" Назначение: Маршрутизатор аутентификации """

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

from src.app.core.config import app_settings
from src.app.core.security import encode_jwt, decode_jwt
from src.app.services.users_services.auth_service import authenticate_user
from src.app.schemas.users_schemas import UserIn
from src.app.core.constants import Token, TokenPayload

# Конфигурация схемы OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')


# Объект роутера
router = APIRouter(tags=["Authentication"])


# Генерация токена
@router.post("/token/", response_model=Token)
async def login_for_access_token(form_data: UserIn):
    """
    Обрабатывает форму логина и выдаёт JWT-токен.
    """
    authenticated_user = await authenticate_user(form_data.email,
                                                 form_data.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials")

    # Формируем нагрузку токена
    jwt_payload = {
        "sub": authenticated_user.email,
        "exp": datetime.utcnow() + timedelta(
            minutes=app_settings.AUTH_JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        "iat": datetime.utcnow()
    }
    token = encode_jwt(jwt_payload)
    return {"access_token": token, "token_type": "bearer"}


# Валидатор токена
def validate_token(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """
    Декодирует токен и проверяет его действительность.
    """
    try:
        decoded_token = decode_jwt(token)
        return TokenPayload(**decoded_token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))


# Текущий активный пользователь
def get_current_user(token_payload: TokenPayload = Depends(validate_token)):
    """
    Возвращает активного пользователя по токену.
    """
    return token_payload.sub


# Контроллер для проверки себя
@router.get("/me/")
async def read_users_me(current_user: str = Depends(get_current_user)):
    """
    Возвращает информацию о текущем авторизованном пользователе.
    """
    return current_user
