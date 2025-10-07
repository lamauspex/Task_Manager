
""" Назначение: Создаёт хэшированный объект пользователя """


from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.users_models import User
from src.app.core.security import hash_password, validate_password
from src.app.schemas.users_schemas import UserCreate, AuthUserIn


async def authenticate_user(
    db: AsyncSession,
    form_data: AuthUserIn
):
    stmt = select(User).where(User.email == form_data.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not validate_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return user


def create_hashed_user(user_create: UserCreate):
    hashed_password = hash_password(user_create.password)
    return {
        **user_create.model_dump(exclude={'password'}),
        'password_hash': hashed_password
    }
