""" Назначение: Общая конфигурация тестов """


import os
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
from fastapi.testclient import TestClient

from src.app.core.database import Base
from src.main import app
from src.app.repositories.users_repo import UsersRepository
from src.app.services.users_services.user_service import UsersService

load_dotenv(dotenv_path=Path('./tests/.env.test'), override=True)


# Асинхронная фикстура для сессий базы данных
@pytest_asyncio.fixture(scope='function')
async def db_session():
    TEST_DATABASE_URL = os.environ["DATABASE_URL"]
    engine = create_async_engine(TEST_DATABASE_URL)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    session_factory = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with session_factory() as session:
        yield session


# Клиент для тестирования API
@pytest.fixture(name="client")
def fixture_client():
    client = TestClient(app)
    return client


# Фикстура для сервиса пользователей
@pytest_asyncio.fixture(scope='function')
async def users_service(db_session: AsyncSession) -> UsersService:
    """Фикстура для сервиса пользователей"""
    repository = UsersRepository(db_session)
    return UsersService(repository)
