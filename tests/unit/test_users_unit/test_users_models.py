
""" Назначение: Тесты моделей USER """


import pytest
import sqlalchemy
from sqlalchemy import select

from src.app.core.constants import Role
from src.app.models.users_models import User
from tests.fixtures.user import UserFactory


@pytest.mark.asyncio
async def test_user_creation(db_session):
    """Проверяет создание и сохранение пользователя в базе данных"""
    new_user = UserFactory.build()
    db_session.add(new_user)
    await db_session.commit()

    retrieved_user = await db_session.get(User, new_user.id)
    assert retrieved_user.first_name == new_user.first_name
    assert retrieved_user.last_name == new_user.last_name
    assert retrieved_user.email == new_user.email
    assert retrieved_user.role == Role.USER
    assert retrieved_user.active is True


@pytest.mark.asyncio
async def test_user_full_name_property():
    """Проверяет вычисляемое свойство full_name"""
    user = UserFactory.build(first_name="Иван", last_name="Петров")
    assert user.full_name == "Иван Петров"


@pytest.mark.asyncio
async def test_user_email_unique_constraint(db_session):
    """Проверяет уникальность email"""
    email = "test@example.com"
    user1 = UserFactory.build(email=email)
    user2 = UserFactory.build(email=email)

    db_session.add(user1)
    await db_session.commit()

    db_session.add(user2)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_user_soft_delete_functionality(db_session):
    """Проверяет функциональность мягкого удаления"""
    user = UserFactory.build()
    db_session.add(user)
    await db_session.commit()

    # Мягкое удаление
    user.is_deleted = True
    user.deleted_at = sqlalchemy.func.now()
    await db_session.commit()

    # Пользователь должен быть в базе, но помечен как удаленный
    retrieved_user = await db_session.get(User, user.id)
    assert retrieved_user.is_deleted is True
    assert retrieved_user.deleted_at is not None


@pytest.mark.asyncio
async def test_user_field_length_constraints():
    """Проверяет ограничения длины полей на уровне Python"""

    # Короткое имя - должно пройти
    user = UserFactory.build(first_name="A")
    assert len(user.first_name) == 1

    # Слишком длинное имя
    with pytest.raises(ValueError):
        UserFactory.build(first_name="A" * 51)

    # Слишком длинная фамилия
    with pytest.raises(ValueError):
        UserFactory.build(last_name="B" * 31)

    # Слишком длинный email
    long_email = "a" * 247 + "@example.com"  # 256 символов
    with pytest.raises(ValueError):
        UserFactory.build(email=long_email)


@pytest.mark.asyncio
async def test_user_role_based_filtering(db_session):
    """Фильтрация пользователей по роли"""
    admin_user = UserFactory.build(role=Role.ADMIN)
    regular_user = UserFactory.build(role=Role.USER)

    db_session.add_all([admin_user, regular_user])
    await db_session.commit()

    # Ищем администраторов
    stmt = select(User).where(User.role == Role.ADMIN)
    result = await db_session.execute(stmt)
    admins = result.scalars().all()

    assert len(admins) == 1
    assert admins[0].role == Role.ADMIN


@pytest.mark.asyncio
async def test_user_bulk_operations(db_session):
    """Массовые операции с пользователями"""
    users = [UserFactory.build() for _ in range(5)]
    db_session.add_all(users)
    await db_session.commit()

    # Проверяем массовое обновление
    stmt = select(User).where(User.active is True)
    result = await db_session.execute(stmt)
    all_users = result.scalars().all()

    # Делаем всех неактивными
    for user in all_users:
        user.active = False

    await db_session.commit()

    # Проверяем изменения
    stmt = select(User).where(User.active is True)
    result = await db_session.execute(stmt)
    active_users = result.scalars().all()

    assert len(active_users) == 0
