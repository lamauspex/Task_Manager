"""
Authentication service.

Handles registration, login, token issuance, and refresh.
All DB calls go through UserRepository — no raw SQLAlchemy here.
"""

import hashlib
import uuid
from datetime import datetime, timedelta, timezone

from backend.src.app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from backend.src.app.core.config import settings
from backend.src.app.core.constants import TokenType
from backend.src.app.exceptions.http import ConflictError, UnauthorizedError
from backend.src.app.models.token import RefreshToken
from backend.src.app.models.user import User
from backend.src.app.repositories.user import UserRepository
from backend.src.app.schemas.auth import LoginRequest, TokenPair
from backend.src.app.schemas.user import UserCreate, UserOut


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._users = user_repo

    async def register(self, data: UserCreate) -> UserOut:
        if await self._users.email_exists(data.email):
            raise ConflictError(f"Email '{data.email}' is already registered")

        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password_hash=hash_password(data.password),
            role=data.role,
        )
        user = await self._users.add(user)
        return UserOut.model_validate(user)

    async def login(self, data: LoginRequest) -> TokenPair:
        user = await self._users.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedError("Account is deactivated")

        return TokenPair(
            access_token=create_access_token(user.email),
            refresh_token=create_refresh_token(user.email),
        )

    async def refresh(self, refresh_token: str) -> TokenPair:
        """Issue a new token pair from a valid refresh token."""
        from jose import JWTError
        try:
            payload = decode_token(refresh_token)
        except JWTError:
            raise UnauthorizedError("Invalid or expired refresh token")

        if payload.get("type") != TokenType.REFRESH:
            raise UnauthorizedError("Token type mismatch")

        email: str = payload.get("sub", "")
        user = await self._users.get_by_email(email)
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or deactivated")

        return TokenPair(
            access_token=create_access_token(user.email),
            refresh_token=create_refresh_token(user.email),
        )

    async def get_current_user(self, token: str) -> User:
        """Decode access token and return the User instance."""
        from jose import JWTError
        try:
            payload = decode_token(token)
        except JWTError:
            raise UnauthorizedError("Invalid or expired token")

        if payload.get("type") != TokenType.ACCESS:
            raise UnauthorizedError("Token type mismatch")

        email: str = payload.get("sub", "")
        user = await self._users.get_by_email(email)
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or deactivated")
        return user
