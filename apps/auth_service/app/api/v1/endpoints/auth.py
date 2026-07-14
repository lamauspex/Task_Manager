"""
Endpoints аутентификации — регистрация, вход, обновление токена, профиль.

Все endpoint's связанные с аутентификацией пользователей.
Использует AuthService для бизнес-логики.
"""


from fastapi import APIRouter, Depends

from backend.src.app.api.dependencies.auth import CurrentUser
from backend.src.app.api.dependencies.services import get_auth_service
from backend.src.app.schemas.auth import LoginRequest, RefreshRequest, TokenPair
from backend.src.app.schemas.user import UserCreate, UserOut
from backend.src.app.services.auth.service import AuthService


router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
    )


@router.post(
    "/register",
    response_model=UserOut,
    status_code=201,
    summary="Register a new user"
)
async def register(
    data: UserCreate,
    service: AuthService = Depends(get_auth_service),
) -> UserOut:
    """
    Регистрация нового пользователя

    Args:
        data: Данные пользователя (email, password, имя)
        service: Сервис аутентификации (внедряется автоматически)
    Returns:
        UserOut: Данные созданного пользователя
    """
    # Вызываем метод регистрации сервиса
    return await service.register(data)


@router.post(
    "/login",
    response_model=TokenPair,
    summary="Login and receive token pair"
)
async def login(
    data: LoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> TokenPair:
    """
    Аутентификация пользователя и получение токенов

    Args:
        data: Учётные данные (email, password)
        service: Сервис аутентификации
    Returns:
        TokenPair: Access и refresh токены
    """
    return await service.login(data)


@router.post(
    "/refresh",
    response_model=TokenPair,
    summary="Refresh access token"
)
async def refresh_tokens(
    data: RefreshRequest,
    service: AuthService = Depends(get_auth_service),
) -> TokenPair:
    """
    Обновление access токена с помощью refresh токена

    Args:
        data: Refresh токен из тела запроса
        service: Сервис аутентификации
    Returns:
        TokenPair: Новая пара токенов
    """
    return await service.refresh(data.refresh_token)


@router.get(
    "/me",  # GET /api/v1/auth/me
    response_model=UserOut,
    summary="Get current user profile" 
)
async def me(
    current_user: CurrentUser, 
) -> UserOut:
    """
    Получение профиля текущего аутентифицированного пользователя

    Args:
        current_user: Данные текущего пользователя (из JWT токена)
    Returns:
        UserOut: Профиль пользователя
    """
    # Преобразуем модель пользователя в схему ответа
    return UserOut.model_validate(current_user)
