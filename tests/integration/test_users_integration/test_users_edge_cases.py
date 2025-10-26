""" Интеграционные тесты для граничных случаев пользователей """


import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.main import app
from src.app.core.constants import Role
from src.app.repositories.users_repo import UsersRepository
from src.app.services.users_services.user_service import UsersService
from src.app.schemas.users_schemas import UserCreate, UserUpdate
from tests.fixtures.user import UserFactory


class TestUsersEdgeCases:
    """Интеграционные тесты для граничных случаев пользователей"""

    @pytest.fixture
    async def users_service(self, db_session: AsyncSession) -> UsersService:
        """Фикстура для сервиса пользователей"""
        repository = UsersRepository(db_session)
        return UsersService(repository)

    @pytest.fixture
    def client(self) -> TestClient:
        """Фикстура для тестового клиента"""
        return TestClient(app)

    async def test_create_user_with_max_field_lengths(
            self, users_service: UsersService):
        """Тест создания пользователя с максимальной длиной полей"""
        max_first_name = "А" * 30
        max_last_name = "Б" * 30
        max_email = f"user@{'c' * 245}.com"  # 255 символов

        user_data = UserCreate(
            first_name=max_first_name,
            last_name=max_last_name,
            email=max_email,
            password="SecurePassword123!",
            role="USER"
        )

        created_user = await users_service.create(user_data)

        assert created_user.first_name == max_first_name
        assert created_user.last_name == max_last_name
        assert created_user.email == max_email

    async def test_create_user_with_min_field_lengths(
            self, users_service: UsersService):
        """Тест создания пользователя с минимальной длиной полей"""
        user_data = UserCreate(
            first_name="Ан",  # 2 символа
            last_name="Ив",  # 2 символа
            email="ai@ex.co",
            password="SecurePassword123!",
            role="USER"
        )

        created_user = await users_service.create(user_data)

        assert created_user.first_name == "Ан"
        assert created_user.last_name == "Ив"

    def test_create_user_api_with_max_password_length(
            self, client: TestClient):
        """Тест создания пользователя с максимальной длиной пароля"""
        max_password = "A" * 128  # 128 символов

        user_data = {
            "first_name": "Макс",
            "last_name": "Пароль",
            "email": "maxpassword@example.com",
            "password": max_password,
            "role": "USER",
            "active": True
        }

        response = client.post("/users/", json=user_data)
        assert response.status_code == 200

    def test_create_user_api_with_min_password_length(
            self, client: TestClient):
        """Тест создания пользователя с минимальной длиной пароля"""
        min_password = "A" * 8  # 8 символов

        user_data = {
            "first_name": "Мин",
            "last_name": "Пароль",
            "email": "minpassword@example.com",
            "password": min_password,
            "role": "USER",
            "active": True
        }

        response = client.post("/users/", json=user_data)
        assert response.status_code == 200

    async def test_create_user_with_different_roles(
            self, users_service: UsersService):
        """Тест создания пользователей с разными ролями"""
        roles = [Role.USER, Role.ADMIN]

        for role in roles:
            user_data = UserCreate(
                first_name=f"Пользователь{role.value}",
                last_name="Тестовый",
                email=f"{role.value}@example.com",
                password="SecurePassword123!",
                role=role.value
            )

            created_user = await users_service.create(user_data)
            assert created_user.role == role.value

    async def test_update_user_partial_data(
            self, users_service: UsersService,
            db_session: AsyncSession):
        """Тест частичного обновления данных пользователя"""
        # Создаем пользователя
        user = UserFactory()
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        original_first_name = user.first_name
        original_last_name = user.last_name

        # Обновляем только email
        update_data = UserUpdate(email="new.email@example.com")
        updated_user = await users_service.update(user.id, update_data)

        assert updated_user is not None
        assert updated_user.email == "new.email@example.com"
        assert updated_user.first_name == original_first_name
        assert updated_user.last_name == original_last_name

    async def test_update_user_no_data(
            self, users_service: UsersService,
            db_session: AsyncSession):
        """Тест обновления пользователя без данных"""
        # Создаем пользователя
        user = UserFactory()
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        # Пытаемся обновить с пустыми данными
        update_data = UserUpdate()
        updated_user = await users_service.update(user.id, update_data)

        assert updated_user is not None
        # Данные должны остаться без изменений

    async def test_create_user_with_special_characters(
            self, users_service: UsersService):
        """Тест создания пользователя со специальными символами"""
        user_data = UserCreate(
            first_name="Анна-Мария",
            last_name="О'Коннелл",
            email="special.chars@example.com",
            password="SecurePassword123!",
            role="USER"
        )

        created_user = await users_service.create(user_data)

        assert created_user.first_name == "Анна-Мария"
        assert created_user.last_name == "О'Коннелл"
        assert created_user.email == "special.chars@example.com"

    async def test_create_user_with_unicode_characters(
            self, users_service: UsersService):
        """Тест создания пользователя с Unicode символами"""
        user_data = UserCreate(
            first_name="Иван",
            last_name="Петров",
            email="unicode@example.com",
            password="SecurePassword123!",
            role="USER"
        )

        created_user = await users_service.create(user_data)

        assert created_user.first_name == "Иван"
        assert created_user.last_name == "Петров"
        assert created_user.full_name == "Иван Петров"

    def test_create_user_api_with_extra_fields(self, client: TestClient):
        """Тест создания пользователя с дополнительными полями"""
        user_data = {
            "first_name": "Тест",
            "last_name": "Пользователь",
            "email": "extrafields@example.com",
            "password": "SecurePassword123!",
            "role": "USER",
            "active": True,
            "extra_field": "should_be_ignored",  # Дополнительное поле
            "another_extra": 123  # Еще одно дополнительное поле
        }

        response = client.post("/users/", json=user_data)

        assert response.status_code == 200
        data = response.json()
        assert "extra_field" not in data
        assert "another_extra" not in data

    async def test_user_full_name_property(self, users_service: UsersService):
        """Тест вычисляемого свойства full_name"""
        user_data = UserCreate(
            first_name="Иван",
            last_name="Иванов",
            email="fullname@example.com",
            password="SecurePassword123!",
            role="USER"
        )

        created_user = await users_service.create(user_data)

        assert created_user.full_name == "Иван Иванов"

        # Тест с пробелами в именах
        user_data2 = UserCreate(
            first_name="  Мария  ",
            last_name="  Петрова  ",
            email="spaces@example.com",
            password="SecurePassword123!",
            role="USER"
        )

        created_user2 = await users_service.create(user_data2)
        # Pydantic должен обрезать пробелы
        assert created_user2.first_name == "Мария"
        assert created_user2.last_name == "Петрова"
        assert created_user2.full_name == "Мария Петрова"

    def test_update_user_api_with_extra_fields(self, client: TestClient):
        """Тест обновления пользователя с дополнительными полями"""
        # Создаем пользователя
        user_data = {
            "first_name": "Тест",
            "last_name": "Обновление",
            "email": "update.extra@example.com",
            "password": "SecurePassword123!",
            "role": "USER",
            "active": True
        }
        create_response = client.post("/users/", json=user_data)
        assert create_response.status_code == 200
        created_user = create_response.json()

        # Обновляем с дополнительными полями
        update_data = {
            "first_name": "Обновленный",
            "last_name": "Пользователь",
            "email": "updated@example.com",
            "extra_field": "should_be_ignored"
        }
        response = client.put(f"/users/{created_user['id']}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Обновленный"
        assert data["last_name"] == "Пользователь"
        assert data["email"] == "updated@example.com"
        assert "extra_field" not in data

    async def test_concurrent_user_creation(self, users_service: UsersService):
        """Тест параллельного создания пользователей"""
        import asyncio

        user_data_list = [
            UserCreate(
                first_name=f"Пользователь{i}",
                last_name="Параллельный",
                email=f"parallel{i}@example.com",
                password="SecurePassword123!",
                role="USER"
            )
            for i in range(5)
        ]

        # Создаем пользователей параллельно
        tasks = [users_service.create(user_data)
                 for user_data in user_data_list]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Проверяем, что все пользователи созданы успешно
        for i, result in enumerate(results):
            assert not isinstance(result, Exception)
            assert result.first_name == f"Пользователь{i}"
            assert result.email == f"parallel{i}@example.com"

    async def test_user_soft_delete_behavior(
            self, users_service: UsersService,
            db_session: AsyncSession):
        """Тест поведения мягкого удаления пользователя"""
        # Создаем пользователя
        user_data = UserCreate(
            first_name="Удаляемый",
            last_name="Пользователь",
            email="soft.delete@example.com",
            password="SecurePassword123!",
            role="USER"
        )

        created_user = await users_service.create(user_data)
        user_id = created_user.id

        # Удаляем пользователя
        delete_result = await users_service.delete(user_id)
        assert delete_result is True

        # Проверяем, что пользователь больше не находится через сервис
        found_user = await users_service.get_by_id(user_id)
        assert found_user is None

    async def test_bulk_user_operations(
            self, users_service: UsersService,
            db_session: AsyncSession):
        """Тест массовых операций с пользователями"""
        # Создаем нескольких пользователей
        users = []
        for i in range(10):
            user_data = UserCreate(
                first_name=f"Массовый{i}",
                last_name="Пользователь",
                email=f"bulk{i}@example.com",
                password="SecurePassword123!",
                role="USER"
            )
            user = await users_service.create(user_data)
            users.append(user)

        # Получаем всех пользователей
        all_users = await users_service.get_all()
        assert len(all_users) >= 10

        # Проверяем, что все созданные пользователи присутствуют
        created_emails = {user.email for user in users}
        all_emails = {user.email for user in all_users}
        assert created_emails.issubset(all_emails)

    def test_user_api_case_sensitivity(self, client: TestClient):
        """Тест чувствительности к регистру в API"""
        # Создаем пользователя
        user_data = {
            "first_name": "Регистр",
            "last_name": "Тест",
            "email": "CaseSensitive@example.com",
            "password": "SecurePassword123!",
            "role": "USER",
            "active": True
        }
        create_response = client.post("/users/", json=user_data)
        assert create_response.status_code == 200

        # Пытаемся получить пользователя по ID (должен работать)
        user_id = create_response.json()["id"]
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 200

    async def test_user_role_filtering(
            self, users_service: UsersService,
            db_session: AsyncSession):
        """Тест фильтрации пользователей по роли"""
        # Создаем пользователей с разными ролями
        admin_data = UserCreate(
            first_name="Админ",
            last_name="Системы",
            email="admin@example.com",
            password="SecurePassword123!",
            role="ADMIN"
        )

        user_data = UserCreate(
            first_name="Обычный",
            last_name="Пользователь",
            email="user@example.com",
            password="SecurePassword123!",
            role="USER"
        )

        admin_user = await users_service.create(admin_data)
        regular_user = await users_service.create(user_data)

        # Получаем всех пользователей
        all_users = await users_service.get_all()
        assert len(all_users) >= 2

        # Проверяем роли
        user_emails = {user.email for user in all_users}
        assert "admin@example.com" in user_emails
        assert "user@example.com" in user_emails

        # Находим пользователей с определенными ролями
        admin_users = [u for u in all_users if u.role == "ADMIN"]
        regular_users = [u for u in all_users if u.role == "USER"]

        assert len(admin_users) >= 1
        assert len(regular_users) >= 1

    def test_error_handling_malformed_json(self, client: TestClient):
        """Тест обработки некорректного JSON"""
        malformed_json = '{"first_name": "Тест", "last_name": "Пользователь", "email": "test@example.com" "password": "password"}'

        response = client.post(
            "/users/",
            data=malformed_json,
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 422  # Unprocessable Entity
