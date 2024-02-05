from typing import AsyncGenerator

from aioredis import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, REDIS_URL

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


pool = ConnectionPool.from_url(REDIS_URL)


def get_redis() -> Redis:
    """Соединение с redis"""
    return Redis(connection_pool=pool)
