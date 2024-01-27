import pytest
from uuid import UUID
from httpx import AsyncClient

from tests.fixtures import prepare_database


@pytest.mark.asyncio
async def test_create_menu_postman(ac: AsyncClient, id_dict):
    """POST - Создает меню"""

    menu_data = {"title": "m title", "description": "m description"}
    response = await ac.post("api/v1/menus/", json=menu_data)

    assert response.status_code == 201

    menu = response.json()

    assert menu["id"] and UUID(menu["id"], version=4)
    assert isinstance(menu["title"], str) and menu["title"] == "m title"
    assert (
        isinstance(menu["description"], str) and menu["description"] == "m description"
    )
    assert isinstance(menu["submenus_count"], int) and menu["submenus_count"] == 0
    assert isinstance(menu["dishes_count"], int) and menu["dishes_count"] == 0

    id_dict["menu_id"] = menu["id"]


@pytest.mark.asyncio
async def test_create_submenu_postman(ac: AsyncClient, id_dict):
    """POST - Создает подменю"""

    submenu_data = {"title": "sm title", "description": "sm description"}
    response = await ac.post(
        f"api/v1/menus/{id_dict['menu_id']}/submenus/", json=submenu_data
    )

    assert response.status_code == 201

    submenu = response.json()

    assert submenu["id"] and UUID(submenu["id"], version=4)
    assert isinstance(submenu["title"], str) and submenu["title"] == "sm title"
    assert (
        isinstance(submenu["description"], str)
        and submenu["description"] == "sm description"
    )
    assert isinstance(submenu["dishes_count"], int) and submenu["dishes_count"] == 0

    id_dict["submenu_id"] = submenu["id"]


@pytest.mark.asyncio
async def test_create_dish1_postman(ac: AsyncClient, id_dict):
    """POST - Создает блюдо 1"""

    dish_data = {"title": "d1 title", "description": "d1 description", "price": 34.99}
    response = await ac.post(
        f"api/v1/menus/{id_dict['menu_id']}/submenus/{id_dict['submenu_id']}/dishes/",
        json=dish_data,
    )

    assert response.status_code == 201

    dish = response.json()

    assert dish["id"] and UUID(dish["id"], version=4)
    assert isinstance(dish["title"], str) and dish["title"] == "d1 title"
    assert (
        isinstance(dish["description"], str) and dish["description"] == "d1 description"
    )
    assert isinstance(dish["price"], str) and dish["price"] == "34.99"


@pytest.mark.asyncio
async def test_create_dish2_postman(ac: AsyncClient, id_dict):
    """POST - Создает блюдо 2"""

    dish_data = {"title": "d2 title", "description": "d2 description", "price": 35.99}
    response = await ac.post(
        f"api/v1/menus/{id_dict['menu_id']}/submenus/{id_dict['submenu_id']}/dishes/",
        json=dish_data,
    )

    assert response.status_code == 201

    dish = response.json()

    assert dish["id"] and UUID(dish["id"], version=4)
    assert isinstance(dish["title"], str) and dish["title"] == "d2 title"
    assert (
        isinstance(dish["description"], str) and dish["description"] == "d2 description"
    )
    assert isinstance(dish["price"], str) and dish["price"] == "35.99"


@pytest.mark.asyncio
async def test_get_specific_menu_postman(ac: AsyncClient, id_dict):
    """GET - просматривает определенное меню"""

    response = await ac.get(f"api/v1/menus/{id_dict['menu_id']}")

    assert response.status_code == 200

    menu = response.json()

    assert menu["id"] and UUID(menu["id"], version=4)
    assert isinstance(menu["title"], str) and menu["title"] == "m title"
    assert (
        isinstance(menu["description"], str) and menu["description"] == "m description"
    )
    assert isinstance(menu["submenus_count"], int) and menu["submenus_count"] == 1
    assert isinstance(menu["dishes_count"], int) and menu["dishes_count"] == 2


@pytest.mark.asyncio
async def test_get_specific_submenu_postman(ac: AsyncClient, id_dict):
    """GET - просматривает определенное подменю"""

    response = await ac.get(
        f"api/v1/menus/{id_dict['menu_id']}/submenus/{id_dict['submenu_id']}"
    )

    assert response.status_code == 200

    submenu = response.json()

    assert submenu["id"] and UUID(submenu["id"], version=4)
    assert isinstance(submenu["title"], str) and submenu["title"] == "sm title"
    assert (
        isinstance(submenu["description"], str)
        and submenu["description"] == "sm description"
    )
    assert isinstance(submenu["dishes_count"], int) and submenu["dishes_count"] == 2


@pytest.mark.asyncio
async def test_delete_submenu_postman(ac: AsyncClient, id_dict):
    """DELETE - Удаляет подменю"""

    response = await ac.delete(
        f"api/v1/menus/{id_dict['menu_id']}/submenus/{id_dict['submenu_id']}"
    )
    assert response.status_code == 200

    response = await ac.get(
        f"api/v1/menus/{id_dict['menu_id']}/submenus/{id_dict['submenu_id']}"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_submenus_postman(ac: AsyncClient, id_dict):
    """GET - просматривает список подменю"""

    response = await ac.get(f"api/v1/menus/{id_dict['menu_id']}/submenus/")

    assert response.status_code == 200
    submenus = response.json()
    assert isinstance(submenus, list)
    assert submenus == []


@pytest.mark.asyncio
async def test_get_all_dishes_postman(ac: AsyncClient, id_dict):
    """GET - просматривает список блюд"""

    response = await ac.get(
        f"api/v1/menus/{id_dict['menu_id']}/submenus/{id_dict['submenu_id']}/dishes/"
    )
    assert response.status_code == 200
    dishes = response.json()
    assert isinstance(dishes, list)
    assert dishes == []


@pytest.mark.asyncio
async def test_get_specific_menu_with_no_childs_postman(ac: AsyncClient, id_dict):
    """GET - просматривает определенное меню"""

    response = await ac.get(f"api/v1/menus/{id_dict['menu_id']}")

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
async def test_delete_menu_postman(ac: AsyncClient, id_dict):
    """DELETE - Удаляет меню"""

    response = await ac.delete(f"api/v1/menus/{id_dict['menu_id']}")
    assert response.status_code == 200

    response = await ac.get(f"api/v1/menus/{id_dict['menu_id']}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_menus_postman(ac: AsyncClient, id_dict):
    """GET - просматривает список меню"""

    response = await ac.get("api/v1/menus/")

    assert response.status_code == 200
    menus = response.json()
    assert isinstance(menus, list)
    assert menus == []
