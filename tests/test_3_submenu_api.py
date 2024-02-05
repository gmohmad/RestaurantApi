from typing import Dict
import pytest
from uuid import UUID, uuid4
from httpx import AsyncClient
from fastapi import HTTPException

from src.models.models import SubMenu
from src.utils import get_submenu_by_id

from tests.conftest import SessionMaker
from tests.reverse import reverse


async def test_create_menu(ac: AsyncClient, ids_storage: Dict[str, str]):
    """POST - тест создания меню"""
    menu_data = {"title": "m title", "description": "m description"}
    response = await ac.post(reverse("create_menu"), json=menu_data)
    assert response.status_code == 201

    ids_storage["menu_id"] = response.json()["id"]


async def test_get_all_submenus_empty(ac: AsyncClient, ids_storage: Dict[str, str]):
    """GET - тест получения всех подменю, когда нет ни одного подменю"""
    response = await ac.get(
        reverse("get_submenus", target_menu_id=ids_storage["menu_id"])
    )

    assert response.status_code == 200
    submenus = response.json()

    assert isinstance(submenus, list)
    assert submenus == []


async def test_create_submenu(ac: AsyncClient, ids_storage: Dict[str, str]):
    """POST - тест создания подменю"""
    submenu_data = {"title": "sm title", "description": "sm description"}
    response = await ac.post(
        reverse("create_submenu", target_menu_id=ids_storage["menu_id"]),
        json=submenu_data,
    )
    submenu = response.json()

    assert response.status_code == 201

    assert submenu["id"] and UUID(submenu["id"], version=4)
    assert submenu["title"] == submenu_data["title"]
    assert submenu["description"] == submenu_data["description"]
    assert submenu["dishes_count"] == 0

    async with SessionMaker() as session:
        db_submenu = await get_submenu_by_id(
            ids_storage["menu_id"], submenu["id"], session
        )

        assert isinstance(db_submenu, SubMenu)
        assert db_submenu.id == UUID(submenu["id"])
        assert db_submenu.title == submenu_data["title"]
        assert db_submenu.description == submenu_data["description"]
        assert db_submenu.dishes_count == 0

    ids_storage["submenu_id"] = submenu["id"]


async def test_get_all_submenus(ac: AsyncClient, ids_storage: Dict[str, str]):
    """GET - тест получения всех подменю"""
    response = await ac.get(
        reverse("get_submenus", target_menu_id=ids_storage["menu_id"])
    )

    assert response.status_code == 200
    submenus = response.json()
    assert isinstance(submenus, list)
    assert len(submenus) == 1

    for submenu in submenus:
        assert submenu["id"] and UUID(submenu["id"], version=4)
        assert isinstance(submenu["title"], str)
        assert isinstance(submenu["description"], str)
        assert isinstance(submenu["dishes_count"], int)


async def test_get_specific_submenu(ac: AsyncClient, ids_storage: Dict[str, str]):
    """GET - тест получения определенного подменю"""
    path_params = {
        "target_menu_id": ids_storage["menu_id"],
        "target_submenu_id": ids_storage["submenu_id"],
    }
    response = await ac.get(reverse("get_submenu", **path_params))

    assert response.status_code == 200
    submenu = response.json()
    assert submenu["id"] == str(ids_storage["submenu_id"])
    assert submenu["title"] == "sm title"
    assert submenu["description"] == "sm description"
    assert submenu["dishes_count"] == 0


async def test_get_specific_submenu_fail(ac: AsyncClient, ids_storage: Dict[str, str]):
    """GET - тест получения несуществующего/некорректного подменю"""
    invalid_id = "yeah for real"
    response = await ac.get(
        reverse(
            "get_submenu",
            target_menu_id=ids_storage["menu_id"],
            target_submenu_id=invalid_id,
        )
    )
    assert response.status_code == 422

    fake_id = uuid4()
    response = await ac.get(
        reverse(
            "get_submenu",
            target_menu_id=ids_storage["menu_id"],
            target_submenu_id=fake_id,
        )
    )
    assert response.status_code == 404


async def test_create_submenu_fail(ac: AsyncClient, ids_storage: Dict[str, str]):
    """POST - тест создания подменю c некорректными данными"""
    invalid_data = {"title": True, "description": False}
    response = await ac.post(
        reverse("create_submenu", target_menu_id=ids_storage["menu_id"]),
        json=invalid_data,
    )
    assert response.status_code == 422


async def test_update_submenu(ac: AsyncClient, ids_storage: Dict[str, str]):
    """PATCH - тест обновления определенного подменю"""
    new_submenu_data = {"title": "new title"}
    path_params = {
        "target_menu_id": ids_storage["menu_id"],
        "target_submenu_id": ids_storage["submenu_id"],
    }
    response = await ac.patch(
        reverse("update_submenu", **path_params), json=new_submenu_data
    )

    assert response.status_code == 200

    submenu = response.json()

    assert submenu["id"] == str(ids_storage["submenu_id"])
    assert submenu["title"] == new_submenu_data["title"]
    assert submenu["description"] == "sm description"
    assert submenu["dishes_count"] == 0

    async with SessionMaker() as session:
        db_submenu = await get_submenu_by_id(
            ids_storage["menu_id"], submenu["id"], session
        )

        assert isinstance(db_submenu, SubMenu)
        assert db_submenu.id == UUID(submenu["id"])
        assert db_submenu.title == new_submenu_data["title"]
        assert db_submenu.description == "sm description"
        assert db_submenu.dishes_count == 0


async def test_update_submenu_fail(ac: AsyncClient, ids_storage: Dict[str, str]):
    """PATCH - тест обновления определенного подменю c некорректными данными"""
    invalid_data = {"title": -1}
    path_params = {
        "target_menu_id": ids_storage["menu_id"],
        "target_submenu_id": ids_storage["submenu_id"],
    }
    response = await ac.patch(
        reverse("update_submenu", **path_params),
        json=invalid_data,
    )

    assert response.status_code == 422


async def test_delete_submenu(ac: AsyncClient, ids_storage: Dict[str, str]):
    """DELETE - тест удаления определенного подменю"""
    path_params = {
        "target_menu_id": ids_storage["menu_id"],
        "target_submenu_id": ids_storage["submenu_id"],
    }
    response = await ac.delete(reverse("delete_submenu", **path_params))
    assert response.status_code == 200

    with pytest.raises(HTTPException) as exc_info:
        async with SessionMaker() as session:
            await get_submenu_by_id(
                ids_storage["menu_id"], ids_storage["submenu_id"], session
            )

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "submenu not found"


async def test_delete_submenu_fail(ac: AsyncClient, ids_storage: Dict[str, str]):
    """DELETE - тест удаления несуществующего/некорректного подменю"""
    invalid_id = "siuuuuu"
    response = await ac.delete(
        reverse(
            "delete_submenu",
            target_menu_id=ids_storage["menu_id"],
            target_submenu_id=invalid_id,
        )
    )
    assert response.status_code == 422

    fake_id = uuid4()
    response = await ac.delete(
        reverse(
            "delete_submenu",
            target_menu_id=ids_storage["menu_id"],
            target_submenu_id=fake_id,
        )
    )
    assert response.status_code == 404
