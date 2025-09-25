
""" Назначение: Роуты user """


from uuid import UUID
from fastapi import APIRouter, Depends

from src.app.core.utils import get_users_service
from src.app.services.users_services.user_service import UsersService
from src.app.schemas.users_schemas import UserCreate, UserOut, UserUpdate
from src.app.exceptions.decorators import exception_handler

router = APIRouter(prefix="/users", tags=["Users"])


# Регистрация пользователя
@router.post("/",
             response_model=UserOut,
             summary="Регистрация пользователя")
@exception_handler
async def create_user(
    user_data: UserCreate,
    service: UsersService = Depends(get_users_service)
):

    new_user = await service.create(user_data)
    return new_user


# Обновление профиля пользователя
@router.put("/{user_id}",
            response_model=UserOut,
            summary="Обновить профиль")
@exception_handler
async def update_user(
    user_id: UUID,
    updated_user: UserUpdate,
    service: UsersService = Depends(get_users_service)
):
    updated_profile = await service.update(user_id, updated_user)
    return updated_profile


# Получение пользователя по id
@router.get("/{user_id}",
            response_model=UserOut,
            summary="Получение информации о пользователе")
@exception_handler
async def get_user_info(
    user_id: UUID,
    service: UsersService = Depends(get_users_service)
):

    return await service.get_by_id(user_id)


# Возвращает список всех зарегистрированных пользователей
@router.get("/",
            response_model=list[UserOut],
            summary="Список всех пользователей")
@exception_handler
async def list_users(
    service: UsersService = Depends(get_users_service)
):

    return await service.get_all()


# Удаляет пользователя по указанному ID
@router.delete("/{user_id}",
               summary="Удаление пользователя")
@exception_handler
async def remove_user(
    user_id: UUID,
    service: UsersService = Depends(get_users_service)
):

    success = await service.delete(user_id)
    return success
