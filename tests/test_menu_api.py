import pytest
from uuid import UUID, uuid4
from httpx import AsyncClient

from tests.conftest import prepare_database


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
    menu = get_test_menu
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
    menu = get_test_menu

    response = await ac.get(detail_path.format(menu.id))

    assert response.status_code == 200

    menu = response.json()

    assert menu["id"] and UUID(menu["id"], version=4)
    assert isinstance(menu["title"], str) and menu["title"] == "m title"
    assert (
        isinstance(menu["description"], str) and menu["description"] == "m description"
    )
    assert isinstance(menu["submenus_count"], int) and menu["submenus_count"] == 0
    assert isinstance(menu["dishes_count"], int) and menu["dishes_count"] == 0


@pytest.mark.asyncio
async def test_get_specific_menu_fail(ac: AsyncClient):
    """GET - тест получения несуществующего/некорректного меню"""

    invalid_id = "gotta_get_that_internship"
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
    assert isinstance(menu["title"], str) and menu["title"] == "m title"
    assert (
        isinstance(menu["description"], str) and menu["description"] == "m description"
    )
    assert isinstance(menu["submenus_count"], int) and menu["submenus_count"] == 0
    assert isinstance(menu["dishes_count"], int) and menu["dishes_count"] == 0


@pytest.mark.asyncio
async def test_create_menu_fail(ac: AsyncClient):
    """POST - тест создания меню с некорректными данными"""

    invalid_data = {"title": 12, "description": None}
    response = await ac.post(list_path, json=invalid_data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_menu(ac: AsyncClient, get_test_menu):
    """PATCH - тест обновления определенного меню"""
    menu = get_test_menu

    new_menu_data = {"title": "new title"}
    response = await ac.patch(detail_path.format(menu.id), json=new_menu_data)

    assert response.status_code == 200

    menu = response.json()

    assert menu["id"] and UUID(menu["id"], version=4)
    assert isinstance(menu["title"], str) and menu["title"] == "new title"
    assert (
        isinstance(menu["description"], str) and menu["description"] == "m description"
    )
    assert isinstance(menu["submenus_count"], int) and menu["submenus_count"] == 0
    assert isinstance(menu["dishes_count"], int) and menu["dishes_count"] == 0


@pytest.mark.asyncio
async def test_update_menu_fail(ac: AsyncClient, get_test_menu):
    """PATCH - тест обновления определенного меню c некорректными данными"""
    menu = get_test_menu

    invalid_data = {"description": 12}
    response = await ac.patch(detail_path.format(menu.id), json=invalid_data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_menu(ac: AsyncClient, get_test_menu):
    """DELETE - тест удаления определенного меню"""
    menu = get_test_menu

    response = await ac.delete(detail_path.format(menu.id))
    assert response.status_code == 200

    get_resp = await ac.get(detail_path.format(menu.id))
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_menu_fail(ac: AsyncClient):
    """DELETE - тест удаления несуществующего/некорректного меню"""

    invalid_id = "some random stuff"
    response = await ac.delete(detail_path.format(invalid_id))
    assert response.status_code == 422

    fake_id = uuid4()
    get_resp = await ac.delete(detail_path.format(fake_id))
    assert get_resp.status_code == 404
