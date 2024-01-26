import pytest
from uuid import UUID, uuid4
from httpx import AsyncClient

from tests.conftest import prepare_database


list_path = "api/v1/menus/{}/submenus/"
detail_path = "api/v1/menus/{}/submenus/{}"


@pytest.mark.asyncio
async def test_get_all_submenus_empty(ac: AsyncClient, get_test_menu):
    """GET - тест получения всех подменю, когда нет ни одного подменю"""
    menu = get_test_menu

    response = await ac.get(list_path.format(menu.id))

    assert response.status_code == 200
    submenus = response.json()

    assert isinstance(submenus, list)
    assert submenus == []


@pytest.mark.asyncio
async def test_get_all_submenus(ac: AsyncClient, get_test_submenu):
    """GET - тест получения всех подменю"""
    menu, submenu = get_test_submenu

    response = await ac.get(list_path.format(menu.id))

    assert response.status_code == 200
    submenus = response.json()
    assert isinstance(submenus, list)
    assert len(submenus) == 1

    for submenu in submenus:
        assert submenu["id"] and UUID(submenu["id"], version=4)
        assert isinstance(submenu["title"], str)
        assert isinstance(submenu["description"], str)
        assert isinstance(submenu["dishes_count"], int)


@pytest.mark.asyncio
async def test_get_specific_submenu(ac: AsyncClient, get_test_submenu):
    """GET - тест получения определенного подменю"""
    menu, submenu = get_test_submenu

    response = await ac.get(detail_path.format(menu.id, submenu.id))

    assert response.status_code == 200

    submenu = response.json()

    assert submenu["id"] and UUID(submenu["id"], version=4)
    assert isinstance(submenu["title"], str) and submenu["title"] == "sm title"
    assert (
        isinstance(submenu["description"], str)
        and submenu["description"] == "sm description"
    )
    assert isinstance(submenu["dishes_count"], int) and submenu["dishes_count"] == 0


@pytest.mark.asyncio
async def test_get_specific_submenu_fail(ac: AsyncClient, get_test_menu):
    """GET - тест получения несуществующего/некорректного подменю"""
    menu = get_test_menu

    invalid_id = "yeah for real"
    response = await ac.get(detail_path.format(menu.id, invalid_id))

    assert response.status_code == 422

    fake_id = uuid4()
    response = await ac.get(detail_path.format(menu.id, fake_id))

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_submenu(ac: AsyncClient, get_test_menu):
    """POST - тест создания подменю"""
    menu = get_test_menu

    submenu_data = {"title": "sm title", "description": "sm description"}
    response = await ac.post(list_path.format(menu.id), json=submenu_data)
    submenu = response.json()

    assert response.status_code == 201

    assert submenu["id"] and UUID(submenu["id"], version=4)
    assert isinstance(submenu["title"], str) and submenu["title"] == "sm title"
    assert (
        isinstance(submenu["description"], str)
        and submenu["description"] == "sm description"
    )
    assert isinstance(submenu["dishes_count"], int) and submenu["dishes_count"] == 0


@pytest.mark.asyncio
async def test_create_submenu_fail(ac: AsyncClient, get_test_menu):
    """POST - тест создания подменю c некорректными данными"""
    menu = get_test_menu

    invalid_data = {"title": True, "description": False}
    response = await ac.post(list_path.format(menu.id), json=invalid_data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_submenu(ac: AsyncClient, get_test_submenu):
    """PATCH - тест обновления определенного подменю"""
    menu, submenu = get_test_submenu

    new_submenu_data = {"title": "new title"}
    response = await ac.patch(
        detail_path.format(menu.id, submenu.id), json=new_submenu_data
    )

    assert response.status_code == 200

    submenu = response.json()

    assert submenu["id"] and UUID(submenu["id"], version=4)
    assert isinstance(submenu["title"], str) and submenu["title"] == "new title"
    assert (
        isinstance(submenu["description"], str)
        and submenu["description"] == "sm description"
    )
    assert isinstance(submenu["dishes_count"], int) and submenu["dishes_count"] == 0


@pytest.mark.asyncio
async def test_update_submenu_fail(ac: AsyncClient, get_test_submenu):
    """PATCH - тест обновления определенного подменю c некорректными данными"""
    menu, submenu = get_test_submenu

    invalid_data = {"title": -1}
    response = await ac.patch(
        detail_path.format(menu.id, submenu.id), json=invalid_data
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_submenu(ac: AsyncClient, get_test_submenu):
    """DELETE - тест удаления определенного подменю"""
    menu, submenu = get_test_submenu
    response = await ac.delete(detail_path.format(menu.id, submenu.id))
    assert response.status_code == 200

    get_resp = await ac.get(detail_path.format(menu.id, submenu.id))
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_submenu_fail(ac: AsyncClient, get_test_menu):
    """DELETE - тест удаления несуществующего/некорректного подменю"""
    menu = get_test_menu

    invalid_id = "siuuuuu"
    response = await ac.delete(detail_path.format(menu.id, invalid_id))
    assert response.status_code == 422

    fake_id = uuid4()
    get_resp = await ac.delete(detail_path.format(menu.id, fake_id))
    assert get_resp.status_code == 404
