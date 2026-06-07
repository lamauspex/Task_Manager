""" API Routers Auth  """


from fastapi import APIRouter, Depends, status

from apps.auth_service.src.api.schemas.auth.requests import LoginRequest
from apps.auth_service.src.api.schemas.auth.responses import TokenResponse


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/login",
    summary="Аутентификация пользователя",
    description="Вход в систему с помощью email и пароля",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Неверные учетные данные"}
    }
)
async def login_user(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    """
    Аутентификация и создание токенов
    """
    # Вызываем метод аутентификации с распакованными данными
    token_pair = auth_service.authenticate_and_create_tokens(
        email=login_data.email,
        password=login_data.password
    )

    return TokenResponse.model_validate(token_pair.to_repository_dict())
