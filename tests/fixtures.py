import asyncio
from typing import Generator

import pytest
from httpx import AsyncClient

from src.database import get_async_session
from src.main import app
from src.model_definitions.models import metadata
from tests.conftest import engine_test, override_session_db


@pytest.fixture(scope='session')
def event_loop(request) -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Создает экземпляр стандартного цикла событий"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope='function')
async def prepare_database() -> None:
    """Фикстура для подготовки тестовой базы данных"""
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)


@pytest.fixture(scope='function')
async def restore_database() -> None:
    """Фикстура для очистки тестовой базы данных"""
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)


@pytest.fixture(scope='session')
async def ac() -> AsyncClient:
    """Фикстура, предоставляющая асинхронный HTTP-клиент (AsyncClient) для тестирования"""
    app.dependency_overrides = {get_async_session: override_session_db}
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture(scope='module')
def ids_storage() -> dict[str, str]:
    """Фикстура для сохранения id объектов"""
    return {}
