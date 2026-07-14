"""User management endpoints."""

import uuid
from fastapi import APIRouter, Depends

from backend.src.app.api.dependencies.auth import AdminUser, CurrentUser
from backend.src.app.api.dependencies.services import get_auth_service
from backend.src.app.repositories.user import UserRepository
from backend.src.app.api.dependencies.services import get_user_repository
from backend.src.app.exceptions.http import NotFoundError
from backend.src.app.schemas.user import UserOut, UserUpdate
from backend.src.app.services.auth.service import AuthService

router = APIRouter(
    prefix="/users", 
    tags=["Users"]
    )


@router.get(
    "/", 
    response_model=list[UserOut], 
    summary="List all users (admin only)"
    )
async def list_users(
    _: AdminUser,
    repo: UserRepository = Depends(get_user_repository),
) -> list[UserOut]:
    users = await repo.get_all()
    return [UserOut.model_validate(u) for u in users]


@router.get(
    "/{user_id}", 
    response_model=UserOut, 
    summary="Get user by ID"
    )
async def get_user(
    user_id: uuid.UUID,
    current_user: CurrentUser,
    repo: UserRepository = Depends(get_user_repository),
) -> UserOut:
    user = await repo.get_by_id(user_id)
    if not user:
        raise NotFoundError("User", str(user_id))
    return UserOut.model_validate(user)


@router.patch(
    "/{user_id}", 
    response_model=UserOut, 
    summary="Update user profile"
    )
async def update_user(
    user_id: uuid.UUID,
    data: UserUpdate,
    current_user: CurrentUser,
    repo: UserRepository = Depends(get_user_repository),
) -> UserOut:
    from backend.src.app.core.constants import Role
    if current_user.role != Role.ADMIN and current_user.id != user_id:
        from backend.src.app.exceptions.http import ForbiddenError
        raise ForbiddenError("You can only update your own profile")

    user = await repo.get_by_id(user_id)
    if not user:
        raise NotFoundError("User", str(user_id))

    update_data = data.model_dump(exclude_unset=True)
    user = await repo.update_fields(user, **update_data)
    return UserOut.model_validate(user)


@router.delete(
    "/{user_id}", 
    status_code=204, 
    summary="Deactivate user (admin only)"
    )
async def deactivate_user(
    user_id: uuid.UUID,
    _: AdminUser,
    repo: UserRepository = Depends(get_user_repository),
) -> None:
    user = await repo.get_by_id(user_id)
    if not user:
        raise NotFoundError("User", str(user_id))
    await repo.update_fields(user, is_active=False)
