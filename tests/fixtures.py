import pytest

from src.schemas.menu_schemas import MenuInput
from src.schemas.submenu_schemas import SubMenuInput
from src.schemas.dish_schemas import DishInput
from src.utils import create_menu_helper, create_submenu_helper, create_dish_helper

from tests.conftest import async_session_maker


@pytest.fixture(scope="function")
async def get_test_menu():
    async with async_session_maker() as session:
        menu = await create_menu_helper(
            MenuInput(title="m title", description="m description"), session
        )
        return menu


@pytest.fixture(scope="function")
async def get_test_submenu():
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
