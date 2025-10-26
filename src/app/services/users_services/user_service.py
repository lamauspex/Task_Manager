""" Назначение: Сервис для работы с пользователями """


from typing import List, Optional
from uuid import UUID

from src.app.core.security import hash_password
from src.app.models.users_models import User
from src.app.repositories.users_repo import UsersRepository
from src.app.schemas.users_schemas import UserCreate, UserOut, UserUpdate
from src.app.interfaces.i_service import IUserService


class UsersService(IUserService):
    """Реализация сервиса для работы с пользователями."""

    def __init__(self, repository: UsersRepository):
        self.repository = repository

    async def create(self, user_data: UserCreate) -> UserOut:
        """ Создание нового пользователя """
        # Получаем хэшированный пароль
        hashed_password = hash_password(user_data.password)
        # Готовим данные для хранения
        user_data_dict = user_data.model_dump()
        user_data_dict.pop('password')
        user_data_dict['password_hash'] = hashed_password

        # Конвертируем enum в строку для хранения в БД
        if 'role' in user_data_dict and hasattr(user_data_dict['role'], 'value'):
            user_data_dict['role'] = user_data_dict['role'].value

        # Передаем данные в репозиторий
        new_user = await self.repository.add(User(**user_data_dict))
        return UserOut.model_validate(new_user)

    async def get_by_id(self, entity_id: UUID) -> Optional[UserOut]:
        """ Получение пользователя по ID """
        user = await self.repository.find_by_id(entity_id)
        if user is None:
            return None
        return UserOut.model_validate(user)

    async def get_all(self) -> List[UserOut]:
        """ Получение всех пользователей """
        users = await self.repository.find_all()
        return [UserOut.model_validate(u) for u in users]

    async def update(self, entity_id: UUID,
                     updated_data: UserUpdate) -> Optional[UserOut]:
        """ Обновление пользователя """
        updated_user = await self.repository.update(entity_id, updated_data)
        return UserOut.model_validate(updated_user)

    async def delete(self, entity_id: UUID) -> bool:
        """ Удаление пользователя """
        return await self.repository.remove(entity_id)
