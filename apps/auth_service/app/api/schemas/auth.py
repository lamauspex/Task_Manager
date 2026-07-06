""" Внутренние DTO для аутентификации (сервисный слой) """



from pydantic import ConfigDict, EmailStr, Field

from backend.src.app.schemas.base import BaseSchema


class LoginRequest(BaseSchema):
    model_config = ConfigDict(str_to_lower=True, str_strip_whitespace=True)

    email: EmailStr
    password: str = Field(min_length=8, max_length=72)




class TokenPair(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseSchema):
    refresh_token: str
