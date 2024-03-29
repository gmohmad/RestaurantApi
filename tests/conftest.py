from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL_TEST = (
    f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

engine_test = create_async_engine(DATABASE_URL_TEST)

SessionMaker = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine_test, class_=AsyncSession
)

pytest_plugins = ['tests.fixtures']


async def override_session_db() -> AsyncSession:
    """Создает экземпляр асинхронной бд сессии"""
    async with SessionMaker() as session:
        yield session
