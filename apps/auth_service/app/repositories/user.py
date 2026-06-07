"""User repository."""

from typing import Optional
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.app.models.user import User
from backend.src.app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model_class = User

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self._session.execute(
            select(User).where(User.email == email.lower())
        )
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        return await self.get_by_email(email) is not None

    async def update_fields(self, user: User, **fields) -> User:
        for key, value in fields.items():
            if value is not None:
                setattr(user, key, value)
        await self._session.flush()
        await self._session.refresh(user)
        return user
