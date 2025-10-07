
""" Назначение: Вспомогательные методы """


from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from jose import jwt, ExpiredSignatureError, JWTError

from src.app.repositories.tasks_repo import TasksRepository
from src.app.repositories.users_repo import UsersRepository
from src.app.services.tasks_service.tasks_service import TasksService
from src.app.services.users_services.user_service import UsersService
from src.app.core.database import get_db
from src.app.core.constants import TokenPayload
from src.app.core.config import app_settings

# Конфигурация схемы OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')


async def get_tasks_service(
    db: AsyncSession = Depends(get_db)
) -> TasksService:
    """ Возвращает экземпляр сервиса задач """
    return TasksService(TasksRepository(db))


async def get_users_service(
    db: AsyncSession = Depends(get_db)
) -> UsersService:
    """ Возвращает экземпляр сервиса пользователя """
    return UsersService(UsersRepository(db))


# Валидатор токена
def validate_token(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    try:
        decoded_token = jwt.decode(
            token, app_settings.SECRET_KEY,
            algorithms=[app_settings.ALGORITHM]
        )
        payload = TokenPayload(**decoded_token)
        now = datetime.now().timestamp()

        if payload.exp < now:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {e}"
        )


# Текущий активный пользователь
def get_current_user(token_payload: TokenPayload = Depends(validate_token)):
    """
    Возвращает активного пользователя по токену
    """
    return token_payload.sub
