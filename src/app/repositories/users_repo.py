
""" Назначение: Реализация репозитория пользователей """


from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID

from src.app.models.users_models import User
from src.app.interfaces.i_repository import IUserRepository
from src.app.schemas.users_schemas import UserUpdate


class UsersRepository(IUserRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: EmailStr) -> Optional[User]:
        """Получение пользователя по email"""
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, user: User) -> User:
        """ Добавление пользователя """
        self.db.add(user)
        await self.db.flush()
        await self.db.commit()
        return user

    async def find_by_id(self, entity_id: UUID) -> Optional[User]:
        """ Поиск по id """
        stmt = select(User).where(User.id == entity_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def find_all(self) -> List[User]:
        """ Получить список пользователей """
        stmt = select(User)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, entity_id: UUID,
                     updates: UserUpdate) -> Optional[User]:
        """ Обновление пользователя """
        user = await self.find_by_id(entity_id)

        if user is None:
            return None

        updates_dict = updates.model_dump(exclude_unset=True)

        for field, value in updates_dict.items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def remove(self, entity_id: UUID) -> bool:
        """ Удаление пользователя """
        user = await self.find_by_id(entity_id)

        if user is None:
            return False

        await self.db.delete(user)
        await self.db.commit()
        return True
