import pytest
from uuid import UUID
from httpx import AsyncClient

from tests.conftest import prepare_database


@pytest.mark.asyncio
async def test_counts_for_menu_and_submenu(ac: AsyncClient):
    """
    Тестовый сценарий «Проверка количества блюд и подменю в меню». 
    Реализовано одним тестом потому, что каждый пункт зависит от предыдущих
    и поэтому нет смысла идти дальше если какой либо пункт упал
    """

    # POST Создает меню
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


    # POST Создает подменю
    submenu_data = {"title": "sm title", "description": "sm description"}
    response = await ac.post(f"api/v1/menus/{menu['id']}/submenus/", json=submenu_data)

    assert response.status_code == 201

    submenu = response.json()

    assert submenu["id"] and UUID(submenu["id"], version=4)
    assert isinstance(submenu["title"], str) and submenu["title"] == "sm title"
    assert (
        isinstance(submenu["description"], str)
        and submenu["description"] == "sm description"
    )
    assert isinstance(submenu["dishes_count"], int) and submenu["dishes_count"] == 0


    # POST Создает блюдо 1
    dish1_data = {"title": "d1 title", "description": "d1 description", "price": 34.99}
    response1 = await ac.post(
        f"api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/", json=dish1_data
    )

    assert response1.status_code == 201

    dish1 = response1.json()

    assert dish1["id"] and UUID(dish1["id"], version=4)
    assert isinstance(dish1["title"], str) and dish1["title"] == "d1 title"
    assert (
        isinstance(dish1["description"], str)
        and dish1["description"] == "d1 description"
    )
    assert isinstance(dish1["price"], str) and dish1["price"] == "34.99"


    # POST Создает блюдо 2
    dish2_data = {"title": "d2 title", "description": "d2 description", "price": 35.99}
    response2 = await ac.post(
        f"api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/", json=dish2_data
    )

    assert response2.status_code == 201

    dish2 = response2.json()

    assert dish2["id"] and UUID(dish2["id"], version=4)
    assert isinstance(dish2["title"], str) and dish2["title"] == "d2 title"
    assert (
        isinstance(dish2["description"], str)
        and dish2["description"] == "d2 description"
    )
    assert isinstance(dish2["price"], str) and dish2["price"] == "35.99"


    # GET просматривает определенное меню
    response = await ac.get(f"api/v1/menus/{menu['id']}")

    assert response.status_code == 200

    menu = response.json()

    assert menu["id"] and UUID(menu["id"], version=4)
    assert isinstance(menu["title"], str) and menu["title"] == "m title"
    assert (
        isinstance(menu["description"], str) and menu["description"] == "m description"
    )
    assert isinstance(menu["submenus_count"], int) and menu["submenus_count"] == 1
    assert isinstance(menu["dishes_count"], int) and menu["dishes_count"] == 2


    # GET просматривает определенное подменю
    response = await ac.get(f"api/v1/menus/{menu['id']}/submenus/{submenu['id']}")

    assert response.status_code == 200

    submenu = response.json()

    assert submenu["id"] and UUID(submenu["id"], version=4)
    assert isinstance(submenu["title"], str) and submenu["title"] == "sm title"
    assert (
        isinstance(submenu["description"], str)
        and submenu["description"] == "sm description"
    )
    assert isinstance(submenu["dishes_count"], int) and submenu["dishes_count"] == 2


    # DEL Удаляет подменю
    response = await ac.delete(f"api/v1/menus/{menu['id']}/submenus/{submenu['id']}")
    assert response.status_code == 200

    response = await ac.get(f"api/v1/menus/{menu['id']}/submenus/{submenu['id']}")
    assert response.status_code == 404


    # GET просматривает список подменю
    response = await ac.get(f"api/v1/menus/{menu['id']}/submenus/")

    assert response.status_code == 200
    submenus = response.json()
    assert isinstance(submenus, list)
    assert submenus == []


    # GET просматривает список блюд
    response = await ac.get(
        f"api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/"
    )

    assert response.status_code == 200
    dishes = response.json()
    assert isinstance(dishes, list)
    assert dishes == []


    # GET просматривает определенное меню
    response = await ac.get(f"api/v1/menus/{menu['id']}")
    assert response.status_code == 200

    menu = response.json()

    assert menu["id"] and UUID(menu["id"], version=4)
    assert isinstance(menu["title"], str) and menu["title"] == "m title"
    assert (
        isinstance(menu["description"], str) and menu["description"] == "m description"
    )
    assert isinstance(menu["submenus_count"], int) and menu["submenus_count"] == 0
    assert isinstance(menu["dishes_count"], int) and menu["dishes_count"] == 0


    # DEL Удаляет меню
    response = await ac.delete(f"api/v1/menus/{menu['id']}")
    assert response.status_code == 200

    response = await ac.get(f"api/v1/menus/{menu['id']}")
    assert response.status_code == 404


    # GET просматривает список меню
    response = await ac.get("api/v1/menus/")

    assert response.status_code == 200
    menus = response.json()
    assert isinstance(menus, list)
    assert menus == []
