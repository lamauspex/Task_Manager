"""
Endpoints аутентификации — регистрация, вход, обновление токена, профиль.

Все endpoint'ы связанные с аутентификацией пользователей.
Использует AuthService для бизнес-логики.
"""

# Импорты FastAPI для роутеров и зависимостей
from fastapi import APIRouter, Depends

# Импорты зависимостей аутентификации
# Тип для текущего пользователя
from backend.src.app.api.dependencies.auth import CurrentUser
# Импорты фабрик сервисов
# Фабрика AuthService
from backend.src.app.api.dependencies.services import get_auth_service

# Импорты схем запросов/ответов аутентификации
from backend.src.app.schemas.auth import LoginRequest, RefreshRequest, TokenPair  # Схемы auth
# Импорты схем пользователя
from backend.src.app.schemas.user import UserCreate, UserOut  # Схемы пользователя

# Импорты сервиса аутентификации
from backend.src.app.services.auth.service import AuthService  # Сервис аутентификации

# Создаём роутер с префиксом /auth и тегом Authentication
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",  # POST /api/v1/auth/register
    response_model=UserOut,  # Модель ответа: данные пользователя
    status_code=201,  # HTTP статус: Created
    summary="Register a new user"  # Краткое описание для Swagger
)
async def register(
    data: UserCreate,  # Данные для регистрации из тела запроса
    # Внедряем сервис через Depends
    service: AuthService = Depends(get_auth_service),
) -> UserOut:
    """
    Регистрация нового пользователя.

    Args:
        data: Данные пользователя (email, password, имя).
        service: Сервис аутентификации (внедряется автоматически).

    Returns:
        UserOut: Данные созданного пользователя.
    """
    # Вызываем метод регистрации сервиса
    return await service.register(data)


@router.post(
    "/login",  # POST /api/v1/auth/login
    response_model=TokenPair,  # Модель ответа: пара токенов
    summary="Login and receive token pair"  # Краткое описание для Swagger
)
async def login(
    data: LoginRequest,  # Данные для входа (email, password)
    # Внедряем сервис через Depends
    service: AuthService = Depends(get_auth_service),
) -> TokenPair:
    """
    Аутентификация пользователя и получение токенов.

    Args:
        data: Учётные данные (email, password).
        service: Сервис аутентификации.

    Returns:
        TokenPair: Access и refresh токены.
    """
    # Вызываем метод входа сервиса
    return await service.login(data)


@router.post(
    "/refresh",  # POST /api/v1/auth/refresh
    response_model=TokenPair,  # Модель ответа: пара токенов
    summary="Refresh access token"  # Краткое описание для Swagger
)
async def refresh_tokens(
    data: RefreshRequest,  # Данные с refresh токеном
    # Внедряем сервис через Depends
    service: AuthService = Depends(get_auth_service),
) -> TokenPair:
    """
    Обновление access токена с помощью refresh токена.

    Args:
        data: Refresh токен из тела запроса.
        service: Сервис аутентификации.

    Returns:
        TokenPair: Новая пара токенов.
    """
    # Вызываем метод обновления токенов сервиса
    return await service.refresh(data.refresh_token)


@router.get(
    "/me",  # GET /api/v1/auth/me
    response_model=UserOut,  # Модель ответа: данные пользователя
    summary="Get current user profile"  # Краткое описание для Swagger
)
async def me(
    current_user: CurrentUser,  # Текущий пользователь (из Depends)
) -> UserOut:
    """
    Получение профиля текущего аутентифицированного пользователя.

    Args:
        current_user: Данные текущего пользователя (из JWT токена).

    Returns:
        UserOut: Профиль пользователя.
    """
    # Преобразуем модель пользователя в схему ответа
    return UserOut.model_validate(current_user)
