
""" Назначение: Тесты схем Pydantic Users """


import uuid
import pytest
from pydantic import ValidationError

from src.app.schemas.users_schemas import (
    UserCreate, UserUpdate,
    UserOut, AuthUserIn
)


def test_user_create_empty_object():
    """ Тестирует создание пользователя с пустым объектом, ожидая ошибку """
    with pytest.raises(ValidationError):
        UserCreate()


def test_user_create_valid():
    """ Тестирует создание пользователя с валидными данными """
    user_data = {
        "first_name": "testuser",
        "last_name": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    UserCreate(**user_data)


def test_user_create_invalid_email():
    """ Тестирует создание пользователя с некорректным email """
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="invalid_email",
            password="testpassword"
        )


def test_user_create_min_max():
    """ Тестирует создание пользователя с минимальным
    и максимальным количеством символов """
    with pytest.raises(ValidationError):
        UserCreate(
            username="a" * 256,
            email="test@example.com",
            password="testpassword"
        )


def test_user_update_empty_object():
    """ Тестирует обновление пользователя
    с пустым объектом, ожидая ошибку """
    with pytest.raises(ValidationError):
        UserUpdate()


def test_user_update_with_extra_fields():
    """ Тестирует обновление пользователя с дополнительными полями,
    должно вызвать ошибку валидации """
    user_data = {
        "first_name": "testuser",
        "last_name": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    with pytest.raises(ValidationError):
        UserUpdate(**user_data)


def test_user_out_model_validate():
    """ Тестирует валидацию модели UserOut """
    user_data = {
        "id": uuid.uuid4(),
        "first_name": "testuser",
        "last_name": "testuser",
        "email": "test@example.com"
    }
    UserOut(**user_data)


def test_user_out_model_validate_with_extra_fields():
    """ Тестирует валидацию модели UserOut с дополнительными полями """
    user_data = {
        "id": uuid.uuid4(),
        "first_name": "testuser",
        "last_name": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    with pytest.raises(ValidationError):
        UserOut(**user_data)


def test_user_login_model_validate():
    """ Тестирует валидацию модели UserLogin """
    user_data = {
        "email": "user@example.com",
        "password": "testpassword"
    }
    AuthUserIn(**user_data)


def test_user_login_model_validate_with_extra_fields():
    """ Тестирует валидацию модели UserLogin с дополнительными полями """
    user_data = {
        "email": "user@example.com",
        "password": "testpassword",
        "user_name": "testuser"
    }
    with pytest.raises(ValidationError):
        AuthUserIn(**user_data)
