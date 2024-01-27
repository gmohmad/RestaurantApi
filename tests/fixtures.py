import pytest
from typing import AsyncGenerator
from httpx import AsyncClient

from src.main import app
from src.models.models import metadata
from src.schemas.menu_schemas import MenuInput
from src.schemas.submenu_schemas import SubMenuInput
from src.schemas.dish_schemas import DishInput
from src.utils import create_menu_helper, create_submenu_helper, create_dish_helper

from tests.conftest import async_session_maker, engine_test


@pytest.fixture(autouse=True, scope="module")
async def prepare_database():
    """Фикстура для подготовки и очистки тестовой базы данных"""
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура, предоставляющая асинхронный HTTP-клиент (AsyncClient) для тестирования"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="module")
def id_dict():
    """Фикстура для сохранения id объектов"""
    return {}


@pytest.fixture(scope="function")
async def get_test_menu():
    """Фикстура для создания меню"""
    async with async_session_maker() as session:
        menu = await create_menu_helper(
            MenuInput(title="m title", description="m description"), session
        )
        return menu


@pytest.fixture(scope="function")
async def get_test_submenu():
    """Фикстура для создания подменю"""
    async with async_session_maker() as session:
        menu = await create_menu_helper(
            MenuInput(title="m title", description="m description"), session
        )
        submenu = await create_submenu_helper(
            menu.id,
            SubMenuInput(title="sm title", description="sm description"),
            session,
        )
        return menu, submenu


@pytest.fixture(scope="function")
async def get_test_dish():
    """Фикстура для создания блюда"""
    async with async_session_maker() as session:
        menu = await create_menu_helper(
            MenuInput(title="m title", description="m description"), session
        )
        submenu = await create_submenu_helper(
            menu.id,
            SubMenuInput(title="sm title", description="sm description"),
            session,
        )
        dish = await create_dish_helper(
            submenu.id,
            DishInput(title="d title", description="d description", price=99.99),
            session,
        )
        return menu, submenu, dish
