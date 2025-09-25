
""" Назначение: Настройка соединения с базой данных """


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator

from src.app.core.config import app_settings


# Создаем асинхронный движок
engine = create_async_engine(app_settings.DATABASE_URL, echo=True)


# Создаем асинхронный sessionmaker
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Создание базового класса
Base = declarative_base()


# Функция создания таблиц
async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Функция для получения сессии
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
