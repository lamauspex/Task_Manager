
""" Назначение: Mетоды, касающиеся безопасности и хэширования паролей """


from jose import jwt
import bcrypt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from src.app.core.config import app_settings


"""  Хэширование паролей  """
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> bytes:
    """
    Хэширует пароль с использованием алгоритма bcrypt.
    Возвращает хешированный пароль в байтах.
    """
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode('utf-8')
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    """
    Проверяет совпадение введённого пароля с заранее хэшированным значением.
    Возвращает True, если совпадает, иначе False.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)


def encode_jwt(payload: dict) -> str:
    """
    Кодирует JSON Web Token с заданной нагрузкой и секретным ключом
    - payload: словарь с информацией, которую хотим сохранить в токене
    - private_key: строка с приватным RSA-кодом
    Возвращает закодированную строку токена.
    """
    current_time = datetime.now()
    expire_time = current_time + \
        timedelta(minutes=app_settings.AUTH_JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = payload.copy()
    to_encode.update({"exp": expire_time, "iat": current_time})
    private_key = app_settings.AUTH_JWT_PRIVATE_KEY_PATH.read_text()
    return jwt.encode(to_encode, private_key,
                      algorithm=app_settings.AUTH_JWT_ALGORITHM)


def decode_jwt(token: str | bytes) -> dict:
    """
    Декодирует токен и возвращает содержимое (payload).
    Если токен недействителен, бросается исключение.
    """
    public_key = app_settings.AUTH_JWT_PUBLIC_KEY_PATH.read_text()
    return jwt.decode(token, public_key,
                      algorithms=[app_settings.AUTH_JWT_ALGORITHM])
