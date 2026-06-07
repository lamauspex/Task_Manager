"""
Модуль хеширования паролей и кодирования/декодирования JWT.

Использует bcrypt для паролей и RS256 асимметричные JWT токены.
Предоставляет access токены (короткоживущие) и refresh токены (долгоживущие).
"""

# Импорты для работы со временем
from datetime import datetime, timedelta, timezone
# Импорты для работы с путями
from pathlib import Path

# Импорты для bcrypt хеширования
import bcrypt
# Импорты для JWT работы
from jose import JWTError, jwt

# Импорты настроек приложения
from backend.src.app.core.config import settings
# Импорты констант типов токенов
from backend.src.app.core.constants import TokenType


# ── Password (Пароли) ────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    """
    Хеширование пароля алгоритмом bcrypt.

    Args:
        plain: Исходный пароль в открытом виде.

    Returns:
        str: Хешированный пароль (UTF-8 строка).
    """
    # Создаём хеш пароля с солью
    hashed = bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())
    # Преобразуем байты в строку для хранения в БД
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """
    Проверка пароля против хеша.

    Args:
        plain: Пароль в открытом виде для проверки.
        hashed: Хешированный пароль из базы данных.

    Returns:
        bool: True если пароль совпадает с хешем.
    """
    # Сравниваем введённый пароль с хешем
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


# ── Helpers (Вспомогательные функции) ────────────────────────────────────────

def _read_key(path: Path) -> str:
    """
    Чтение ключа JWT из файла.

    Args:
        path: Путь к файлу с ключом.

    Returns:
        str: Содержимое файла ключа.

    Raises:
        FileNotFoundError: Если файл ключа не найден.
    """
    # Проверяем существование файла
    if not path.exists():
        raise FileNotFoundError(
            f"JWT ключ не найден в {path}. "
            "Запустите `python scripts/generate_keys.py` для генерации."
        )
    # Читаем содержимое файла
    return path.read_text()


# ── JWT (JSON Web Tokens) ────────────────────────────────────────────────────

def create_access_token(subject: str) -> str:
    """
    Создание короткоживущего access JWT токена.

    Args:
        subject: Email пользователя (или ID) для токена.

    Returns:
        str: JWT токен доступа.
    """
    # Текущее время UTC
    now = datetime.now(timezone.utc)
    # Полезная нагрузка токена
    payload = {
        "sub": subject,  # Субъект (email пользователя)
        "type": TokenType.ACCESS,  # Тип токена
        "iat": now,  # Время создания
        # Время истечения
        "exp": now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    # Кодируем и подписываем токен приватным ключом
    return jwt.encode(payload, _read_key(settings.JWT_PRIVATE_KEY_PATH), algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: str) -> str:
    """
    Создание долгоживущего refresh JWT токена.

    Args:
        subject: Email пользователя (или ID) для токена.

    Returns:
        str: JWT токен обновления.
    """
    # Текущее время UTC
    now = datetime.now(timezone.utc)
    # Полезная нагрузка токена
    payload = {
        "sub": subject,  # Субъект (email пользователя)
        "type": TokenType.REFRESH,  # Тип токена
        "iat": now,  # Время создания
        # Время истечения
        "exp": now + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
    }
    # Кодируем и подписываем токен приватным ключом
    return jwt.encode(payload, _read_key(settings.JWT_PRIVATE_KEY_PATH), algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Декодирование и проверка JWT токена.

    Args:
        token: JWT токен для декодирования.

    Returns:
        dict: Расшифрованная полезная нагрузка токена.

    Raises:
        jose.JWTError: Если токен невалидный или истёк.
    """
    # Декодируем токен с использованием публичного ключа
    return jwt.decode(
        token,
        _read_key(settings.JWT_PUBLIC_KEY_PATH),  # Публичный ключ для проверки
        algorithms=[settings.JWT_ALGORITHM],  # Разрешённые алгоритмы
    )
