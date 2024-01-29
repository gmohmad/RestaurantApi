import pytest
from uuid import UUID, uuid4
from httpx import AsyncClient
from fastapi import HTTPException

from src.models.models import SubMenu
from src.utils import get_counts_for_submenu, get_submenu_by_id
from tests.fixtures import prepare_database
from tests.conftest import async_session_maker

list_path = "api/v1/menus/{}/submenus/"
detail_path = "api/v1/menus/{}/submenus/{}"


@pytest.mark.asyncio
async def test_get_all_submenus_empty(ac: AsyncClient, get_test_menu):
    """GET - тест получения всех подменю, когда нет ни одного подменю"""
    new_menu = get_test_menu

    response = await ac.get(list_path.format(new_menu.id))

    assert response.status_code == 200
    submenus = response.json()

    assert isinstance(submenus, list)
    assert submenus == []


@pytest.mark.asyncio
async def test_get_all_submenus(ac: AsyncClient, get_test_submenu):
    """GET - тест получения всех подменю"""
    new_menu, new_submenu = get_test_submenu

    response = await ac.get(list_path.format(new_menu.id))

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
    new_menu, new_submenu = get_test_submenu

    response = await ac.get(detail_path.format(new_menu.id, new_submenu.id))

    assert response.status_code == 200

    submenu = response.json()

    assert submenu["id"] == str(new_submenu.id)
    assert submenu["title"] == "sm title"
    assert submenu["description"] == "sm description"
    assert submenu["dishes_count"] == 0


@pytest.mark.asyncio
async def test_get_specific_submenu_with_childs(ac: AsyncClient, get_test_dish):
    """GET - тест получения определенного подменю с дочерними объектами"""
    new_menu, new_submenu, new_dish = get_test_dish

    response = await ac.get(detail_path.format(new_menu.id, new_submenu.id))

    assert response.status_code == 200

    submenu = response.json()

    assert submenu["id"] == str(new_submenu.id)
    assert submenu["title"] == "sm title"
    assert submenu["description"] == "sm description"
    assert submenu["dishes_count"] == 1


@pytest.mark.asyncio
async def test_get_specific_submenu_fail(ac: AsyncClient, get_test_menu):
    """GET - тест получения несуществующего/некорректного подменю"""
    new_menu = get_test_menu

    invalid_id = "yeah for real"
    response = await ac.get(detail_path.format(new_menu.id, invalid_id))

    assert response.status_code == 422

    fake_id = uuid4()
    response = await ac.get(detail_path.format(new_menu.id, fake_id))

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_submenu(ac: AsyncClient, get_test_menu):
    """POST - тест создания подменю"""
    new_menu = get_test_menu

    submenu_data = {"title": "sm title", "description": "sm description"}
    response = await ac.post(list_path.format(new_menu.id), json=submenu_data)
    submenu = response.json()

    assert response.status_code == 201

    assert submenu["id"] and UUID(submenu["id"], version=4)
    assert submenu["title"] == submenu_data["title"]
    assert submenu["description"] == submenu_data["description"]
    assert submenu["dishes_count"] == 0

    async with async_session_maker() as session:
        db_submenu = await get_submenu_by_id(new_menu.id, submenu["id"], session)

        assert isinstance(db_submenu, SubMenu)
        assert db_submenu.id == UUID(submenu["id"])
        assert db_submenu.title == submenu_data["title"]
        assert db_submenu.description == submenu_data["description"]

        db_submenu_dishes = await get_counts_for_submenu(db_submenu.id, session)
        assert db_submenu_dishes == 0


@pytest.mark.asyncio
async def test_create_submenu_fail(ac: AsyncClient, get_test_menu):
    """POST - тест создания подменю c некорректными данными"""
    new_menu = get_test_menu

    invalid_data = {"title": True, "description": False}
    response = await ac.post(list_path.format(new_menu.id), json=invalid_data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_submenu(ac: AsyncClient, get_test_submenu):
    """PATCH - тест обновления определенного подменю"""
    new_menu, new_submenu = get_test_submenu

    new_submenu_data = {"title": "new title"}
    response = await ac.patch(
        detail_path.format(new_menu.id, new_submenu.id), json=new_submenu_data
    )

    assert response.status_code == 200

    submenu = response.json()

    assert submenu["id"] == str(new_submenu.id)
    assert submenu["title"] == new_submenu_data["title"]
    assert submenu["description"] == "sm description"
    assert submenu["dishes_count"] == 0

    async with async_session_maker() as session:
        db_submenu = await get_submenu_by_id(new_menu.id, submenu["id"], session)

        assert isinstance(db_submenu, SubMenu)
        assert db_submenu.id == UUID(submenu["id"])
        assert db_submenu.title == new_submenu_data["title"]
        assert db_submenu.description == "sm description"

        db_submenu_dishes = await get_counts_for_submenu(db_submenu.id, session)
        assert db_submenu_dishes == 0


@pytest.mark.asyncio
async def test_update_submenu_fail(ac: AsyncClient, get_test_submenu):
    """PATCH - тест обновления определенного подменю c некорректными данными"""
    new_menu, new_submenu = get_test_submenu

    invalid_data = {"title": -1}
    response = await ac.patch(
        detail_path.format(new_menu.id, new_submenu.id), json=invalid_data
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_submenu(ac: AsyncClient, get_test_submenu):
    """DELETE - тест удаления определенного подменю"""
    new_menu, new_submenu = get_test_submenu
    response = await ac.delete(detail_path.format(new_menu.id, new_submenu.id))
    assert response.status_code == 200

    with pytest.raises(HTTPException) as exc_info:
        async with async_session_maker() as session:
            await get_submenu_by_id(new_menu.id, new_submenu.id, session)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "submenu not found"


@pytest.mark.asyncio
async def test_delete_submenu_fail(ac: AsyncClient, get_test_menu):
    """DELETE - тест удаления несуществующего/некорректного подменю"""
    new_menu = get_test_menu

    invalid_id = "siuuuuu"
    response = await ac.delete(detail_path.format(new_menu.id, invalid_id))
    assert response.status_code == 422

    fake_id = uuid4()
    get_resp = await ac.delete(detail_path.format(new_menu.id, fake_id))
    assert get_resp.status_code == 404
