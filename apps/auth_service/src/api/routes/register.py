""" API Routers Register """

from fastapi import APIRouter, Depends, status

from apps.auth_service.src.api.schemas.register.register_request import UserCreate
from apps.auth_service.src.api.schemas.register.register_response import UserResponseDTO


# Создаем router
router = APIRouter(
    prefix="/register",
    tags=["Register"]
)


@router.post(
    "/register",
    summary="Регистрация пользователя",
    description="Создание нового пользователя",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Пользователь с таким email/именем существует"},
        422: {"description": "Ошибка валидации данных"}
    }
)
async def register_user(
    register_data: UserCreate,
    register_service: RegisterService = Depends(get_register_service)
) -> UserResponseDTO:
    """
    Регистрация пользователя
    Сервис возвращает готовый UserResponseDTO
    """

    return register_service.register_user(register_data)
