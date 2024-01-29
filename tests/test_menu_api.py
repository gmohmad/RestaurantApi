import pytest
from uuid import UUID, uuid4
from httpx import AsyncClient
from fastapi import HTTPException

from src.utils import get_menu_by_id, get_counts_for_menu
from src.models.models import Menu
from tests.conftest import async_session_maker
from tests.fixtures import prepare_database


list_path = "api/v1/menus/"
detail_path = "api/v1/menus/{}"


@pytest.mark.asyncio
async def test_get_all_menus_empty(ac: AsyncClient):
    """GET - тест получения всех меню, когда нет ни одного меню"""
    response = await ac.get(list_path)

    assert response.status_code == 200
    menus = response.json()

    assert isinstance(menus, list)
    assert menus == []


@pytest.mark.asyncio
async def test_get_all_menus(ac: AsyncClient, get_test_menu):
    """GET - тест получения всех меню"""
    new_menu = get_test_menu
    response = await ac.get(list_path)

    assert response.status_code == 200
    menus = response.json()

    assert isinstance(menus, list)
    assert len(menus) == 1

    for menu in menus:
        assert menu["id"] and UUID(menu["id"], version=4)
        assert isinstance(menu["title"], str)
        assert isinstance(menu["description"], str)
        assert isinstance(menu["submenus_count"], int)
        assert isinstance(menu["dishes_count"], int)


@pytest.mark.asyncio
async def test_get_specific_menu(ac: AsyncClient, get_test_menu):
    """GET - тест получения определенного меню"""
    new_menu = get_test_menu

    response = await ac.get(detail_path.format(new_menu.id))

    assert response.status_code == 200

    menu = response.json()

    assert menu["id"] == str(new_menu.id)
    assert menu["title"] == "m title"
    assert menu["description"] == "m description"
    assert menu["submenus_count"] == 0
    assert menu["dishes_count"] == 0


@pytest.mark.asyncio
async def test_get_specific_menu_with_childs(ac: AsyncClient, get_test_dish):
    """GET - тест получения определенного меню с дочерними объектами"""
    new_menu, new_submenu, new_dish = get_test_dish # *_

    response = await ac.get(detail_path.format(new_menu.id))

    assert response.status_code == 200

    menu = response.json()

    assert menu["id"] == str(new_menu.id)
    assert menu["title"] == "m title"
    assert menu["description"] == "m description"
    assert menu["submenus_count"] == 1
    assert menu["dishes_count"] == 1


@pytest.mark.asyncio
async def test_get_specific_menu_fail(ac: AsyncClient):
    """GET - тест получения несуществующего/некорректного меню"""

    invalid_id = "gotta get that internship"
    response = await ac.get(detail_path.format(invalid_id))

    assert response.status_code == 422

    fake_id = uuid4()
    response = await ac.get(detail_path.format(fake_id))

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_menu(ac: AsyncClient):
    """POST - тест создания меню"""
    menu_data = {"title": "m title", "description": "m description"}
    response = await ac.post(list_path, json=menu_data)

    assert response.status_code == 201

    menu = response.json()

    assert menu["id"] and UUID(menu["id"], version=4)
    assert menu["title"] == menu_data["title"]
    assert menu["description"] == menu_data["description"]
    assert menu["submenus_count"] == 0
    assert menu["dishes_count"] == 0

    async with async_session_maker() as session:
        db_menu = await get_menu_by_id(menu["id"], session)

        assert isinstance(db_menu, Menu)
        assert db_menu.id == UUID(menu["id"])
        assert db_menu.title == menu_data["title"]
        assert db_menu.description == menu_data["description"]

        db_menu_counts = await get_counts_for_menu(db_menu.id, session)
        assert db_menu_counts == (0, 0)


@pytest.mark.asyncio
async def test_create_menu_fail(ac: AsyncClient):
    """POST - тест создания меню с некорректными данными"""

    invalid_data = {"title": 12, "description": None}
    response = await ac.post(list_path, json=invalid_data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_menu(ac: AsyncClient, get_test_menu):
    """PATCH - тест обновления определенного меню"""
    new_menu = get_test_menu

    new_menu_data = {"title": "new title"}
    response = await ac.patch(detail_path.format(new_menu.id), json=new_menu_data)

    assert response.status_code == 200

    menu = response.json()

    assert menu["id"] == str(new_menu.id)
    assert menu["title"] == new_menu_data["title"]
    assert menu["description"] == "m description"
    assert menu["submenus_count"] == 0
    assert menu["dishes_count"] == 0

    async with async_session_maker() as session:
        db_menu = await get_menu_by_id(menu["id"], session)

        assert isinstance(db_menu, Menu)
        assert db_menu.id == UUID(menu["id"])
        assert db_menu.title == new_menu_data["title"]
        assert db_menu.description == "m description"

        db_menu_counts = await get_counts_for_menu(db_menu.id, session)
        assert db_menu_counts == (0, 0)


@pytest.mark.asyncio
async def test_update_menu_fail(ac: AsyncClient, get_test_menu):
    """PATCH - тест обновления определенного меню c некорректными данными"""
    new_menu = get_test_menu

    invalid_data = {"description": 12}
    response = await ac.patch(detail_path.format(new_menu.id), json=invalid_data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_menu(ac: AsyncClient, get_test_menu):
    """DELETE - тест удаления определенного меню"""
    new_menu = get_test_menu

    response = await ac.delete(detail_path.format(new_menu.id))
    assert response.status_code == 200

    with pytest.raises(HTTPException) as exc_info:
        async with async_session_maker() as session:
            await get_menu_by_id(new_menu.id, session)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "menu not found"


@pytest.mark.asyncio
async def test_delete_menu_fail(ac: AsyncClient):
    """DELETE - тест удаления несуществующего/некорректного меню"""

    invalid_id = "some random stuff"
    response = await ac.delete(detail_path.format(invalid_id))
    assert response.status_code == 422

    fake_id = uuid4() # the probability of this uuid matching the ids of the other 
                      # menus created duting the runtime of this module is negligible, 
                      # and therefore insignificant
    get_resp = await ac.delete(detail_path.format(fake_id))
    assert get_resp.status_code == 404
