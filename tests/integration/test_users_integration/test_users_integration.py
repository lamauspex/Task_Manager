""" Назначение: Интеграционные тесты для пользователей """


import pytest
import pytest_asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.users_models import User
from src.app.repositories.users_repo import UsersRepository
from src.app.schemas.users_schemas import UserCreate, AuthUserIn
from src.app.services.users_services.auth_service import authenticate_user, create_hashed_user
from tests.fixtures.user import UserFactory


class TestUsersIntegration:
    """Интеграционные тесты для пользователей"""

    @pytest.mark.asyncio
    async def test_create_user_integration(self, users_service, db_session: AsyncSession):
        """Тест создания пользователя через сервис"""
        from src.app.core.constants import Role

        user_data = UserCreate(
            first_name="Иван",
            last_name="Иванов",
            email="ivan.ivanov@example.com",
            password="SecurePassword123!",
            role=Role.USER,
            active=True
        )

        created_user = await users_service.create(user_data)

        assert created_user.first_name == "Иван"
        assert created_user.last_name == "Иванов"
        assert created_user.email == "ivan.ivanov@example.com"
        assert created_user.role == Role.USER
        assert created_user.active is True
        assert created_user.full_name == "Иван Иванов"

    @pytest.mark.asyncio
    async def test_get_user_by_id_integration(self, users_service, db_session: AsyncSession):
        """Тест получения пользователя по ID"""
        # Создаем пользователя через фабрику
        user = UserFactory()
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Получаем через сервис
        found_user = await users_service.get_by_id(user.id)

        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == user.email

    @pytest.mark.asyncio
    async def test_get_user_by_nonexistent_id(self, users_service):
        """Тест получения несуществующего пользователя"""
        nonexistent_id = uuid4()
        found_user = await users_service.get_by_id(nonexistent_id)
        assert found_user is None

    @pytest.mark.asyncio
    async def test_get_all_users_integration(self, users_service, db_session: AsyncSession):
        """Тест получения всех пользователей"""
        # Создаем несколько пользователей
        users = [UserFactory() for _ in range(3)]
        for user in users:
            db_session.add(user)
        await db_session.commit()

        # Получаем всех пользователей
        all_users = await users_service.get_all()

        assert len(all_users) >= 3

    @pytest.mark.asyncio
    async def test_update_user_integration(self, users_service, db_session: AsyncSession):
        """Тест обновления пользователя"""
        # Создаем пользователя
        user = UserFactory()
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Обновляем данные
        from src.app.schemas.users_schemas import UserUpdate
        update_data = UserUpdate(
            first_name="Петр",
            last_name="Петров",
            email="petr.petrov@example.com"
        )

        updated_user = await users_service.update(user.id, update_data)

        assert updated_user is not None
        assert updated_user.first_name == "Петр"
        assert updated_user.last_name == "Петров"

    @pytest.mark.asyncio
    async def test_delete_user_integration(self, users_service, db_session: AsyncSession):
        """Тест удаления пользователя"""
        # Создаем пользователя
        user = UserFactory()
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        user_id = user.id

        # Удаляем пользователя
        delete_result = await users_service.delete(user_id)
        assert delete_result is True

        # Проверяем, что пользователь удален
        deleted_user = await users_service.get_by_id(user_id)
        assert deleted_user is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_user(self, users_service):
        """Тест удаления несуществующего пользователя"""
        nonexistent_id = uuid4()
        delete_result = await users_service.delete(nonexistent_id)
        assert delete_result is False

    def test_create_user_api_endpoint(self, client):
        """Тест создания пользователя через API"""
        import time
        unique_email = f"anna.smirnova.{int(time.time())}@example.com"

        user_data = {
            "first_name": "Анна",
            "last_name": "Смирнова",
            "email": unique_email,
            "password": "SecurePassword123!",
            "role": "USER",
            "active": True
        }

        response = client.post("/users/", json=user_data)

        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Анна"
        assert data["last_name"] == "Смирнова"
        assert data["email"] == unique_email
        assert data["role"] == "USER"
        assert "password" not in data
        assert "full_name" in data

    def test_create_user_api_invalid_data(self, client):
        """Тест создания пользователя с невалидными данными"""
        invalid_data = {
            "first_name": "А",  # Слишком короткое имя
            "last_name": "Смирнова",
            "email": "invalid-email",  # Невалидный email
            "password": "123",  # Слишком короткий пароль
            "role": "USER",
            "active": True
        }

        response = client.post("/users/", json=invalid_data)

        assert response.status_code == 422

    def test_get_user_by_id_api_endpoint(self, client):
        """Тест получения пользователя по ID через API"""
        import time
        unique_email = f"mikhail.kuznetsov.{int(time.time())}@example.com"

        # Сначала создаем пользователя
        user_data = {
            "first_name": "Михаил",
            "last_name": "Кузнецов",
            "email": unique_email,
            "password": "SecurePassword123!",
            "role": "USER",
            "active": True
        }
        create_response = client.post("/users/", json=user_data)
        assert create_response.status_code == 200
        created_user = create_response.json()

        # Получаем пользователя по ID
        response = client.get(f"/users/{created_user['id']}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_user["id"]
        assert data["email"] == unique_email

    def test_get_nonexistent_user_api(self, client):
        """Тест получения несуществующего пользователя через API"""
        nonexistent_id = str(uuid4())
        response = client.get(f"/users/{nonexistent_id}")
        assert response.status_code == 404

    def test_get_all_users_api_endpoint(self, client):
        """Тест получения всех пользователей через API"""
        import time
        # Создаем нескольких пользователей
        users_data = [
            {
                "first_name": "Елена",
                "last_name": "Попова",
                "email": f"elena.popova.{int(time.time())}@example.com",
                "password": "SecurePassword123!",
                "role": "USER",
                "active": True
            },
            {
                "first_name": "Дмитрий",
                "last_name": "Волков",
                "email": f"dmitry.volkov.{int(time.time())}@example.com",
                "password": "SecurePassword123!",
                "role": "USER",
                "active": True
            }
        ]

        for user_data in users_data:
            client.post("/users/", json=user_data)

        # Получаем всех пользователей
        response = client.get("/users/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2

    def test_update_user_api_endpoint(self, client):
        """Тест обновления пользователя через API"""
        import time
        unique_email = f"olga.novikova.{int(time.time())}@example.com"

        # Создаем пользователя
        user_data = {
            "first_name": "Ольга",
            "last_name": "Новикова",
            "email": unique_email,
            "password": "SecurePassword123!",
            "role": "USER",
            "active": True
        }
        create_response = client.post("/users/", json=user_data)
        assert create_response.status_code == 200
        created_user = create_response.json()

        # Обновляем пользователя
        update_data = {
            "first_name": "Ольга Александровна",
            "last_name": "Новикова-Иванова",
            "email": f"olga.ivanova.{int(time.time())}@example.com"
        }
        response = client.put(f"/users/{created_user['id']}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Ольга Александровна"
        assert data["last_name"] == "Новикова-Иванова"

    def test_delete_user_api_endpoint(self, client):
        """Тест удаления пользователя через API"""
        import time
        unique_email = f"alexander.belov.{int(time.time())}@example.com"

        # Создаем пользователя
        user_data = {
            "first_name": "Александр",
            "last_name": "Белов",
            "email": unique_email,
            "password": "SecurePassword123!",
            "role": "USER",
            "active": True
        }
        create_response = client.post("/users/", json=user_data)
        assert create_response.status_code == 200
        created_user = create_response.json()

        # Удаляем пользователя
        response = client.delete(f"/users/{created_user['id']}")

        assert response.status_code == 200
        assert response.json() is True

        # Проверяем, что пользователь удален
        get_response = client.get(f"/users/{created_user['id']}")
        assert get_response.status_code == 404

    def test_get_users_dashboard_list_api(self, client):
        """Тест получения списка пользователей для дашборда"""
        import time
        unique_email = f"sergey.sokolov.{int(time.time())}@example.com"

        # Создаем пользователя
        user_data = {
            "first_name": "Сергей",
            "last_name": "Соколов",
            "email": unique_email,
            "password": "SecurePassword123!",
            "role": "USER",
            "active": True
        }
        client.post("/users/", json=user_data)

        # Получаем список для дашборда
        response = client.get("/users/dashboard/list")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Проверяем форматирование имен
        for user in data:
            assert "id" in user
            assert "full_name" in user
            assert "email" in user
            # Имена должны быть с заглавной буквы
            if user["full_name"]:
                names = user["full_name"].split()
                for name in names:
                    assert name[0].isupper()

    @pytest.mark.asyncio
    async def test_user_email_uniqueness_integration(self, users_service):
        """Тест уникальности email при создании пользователей"""
        import time
        from src.app.core.constants import Role
        timestamp = int(time.time())

        user_data1 = UserCreate(
            first_name="Пользователь1",
            last_name="Тестовый",
            email=f"duplicate{timestamp}@example.com",
            password="SecurePassword123!",
            role=Role.USER
        )

        user_data2 = UserCreate(
            first_name="Пользователь2",
            last_name="Тестовый",
            email=f"duplicate{timestamp}@example.com",  # Тот же email
            password="SecurePassword123!",
            role=Role.USER
        )

        # Создаем первого пользователя
        await users_service.create(user_data1)

        # Попытка создать второго пользователя с тем же email должна вызвать ошибку
        with pytest.raises(Exception):  # Должна быть ошибка целостности базы данных
            await users_service.create(user_data2)
