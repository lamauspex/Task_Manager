
""" Назначение: Создаёт хэшированный объект пользователя """


from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.app.models.users_models import User
from src.app.core.security import hash_password, validate_password
from src.app.schemas.users_schemas import UserCreate


async def authenticate_user(
    db: Session, form_data: OAuth2PasswordRequestForm
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not validate_password(
        form_data.password, user.password_hash
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


def create_hashed_user(user_create: UserCreate):
    hashed_password = hash_password(user_create.password)
    return {
        **user_create.model_dump(exclude={'password'}),
        'password_hash': hashed_password
    }
