"""
Зависимости аутентификации для защиты FastAPI роутов.

Предоставляет функции для получения текущего пользователя и проверки ролей.
"""

from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from apps.auth_service.app.api.dependencies.services import get_auth_service
from apps.auth_service.app.core.constants import Role
from apps.auth_service.app.exceptions.http import ForbiddenError
from apps.auth_service.app.models.user import User
from apps.auth_service.app.services.service import AuthService

# OAuth2 схема для извлечения Bearer токена из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """
    Получение текущего аутентифицированного пользователя из Bearer токена.

    Args:
        token: JWT токен из заголовка Authorization.
        auth_service: Сервис аутентификации.

    Returns:
        User: Модель текущего пользователя.

    Raises:
        HTTPException: Если токен невалидный или истёк.
    """
    # Извлекаем пользователя из токена через сервис
    return await auth_service.get_current_user(token)


async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Проверка роли ADMIN — выбрасывает 403 если не админ.

    Args:
        current_user: Текущий аутентифицированный пользователь.

    Returns:
        User: Текущий пользователь (если админ).

    Raises:
        ForbiddenError: Если у пользователя нет роли ADMIN.
    """
    # Проверяем роль пользователя
    if current_user.role != Role.ADMIN:
        # Если не админ — выбрасываем ошибку 403
        raise ForbiddenError("Требуется доступ администратора")
    # Возвращаем пользователя (админ)
    return current_user


CurrentUser = Annotated[User, Depends(
    get_current_user)]  # Текущий пользователь
AdminUser = Annotated[User, Depends(require_admin)]
