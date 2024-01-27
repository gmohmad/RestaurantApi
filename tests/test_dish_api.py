import pytest
from uuid import UUID, uuid4
from httpx import AsyncClient

from tests.fixtures import prepare_database


list_path = "api/v1/menus/{}/submenus/{}/dishes/"
detail_path = "api/v1/menus/{}/submenus/{}/dishes/{}"


@pytest.mark.asyncio
async def test_get_all_dishes_empty(ac: AsyncClient, get_test_submenu):
    """GET - тест получения всех блюд, когда нет ни одного блюда"""
    menu, submenu = get_test_submenu

    response = await ac.get(list_path.format(menu.id, submenu.id))

    assert response.status_code == 200
    dishes = response.json()

    assert isinstance(dishes, list)
    assert dishes == []


@pytest.mark.asyncio
async def test_get_all_dishes(ac: AsyncClient, get_test_dish):
    """GET - тест получения всех блюд"""
    menu, submenu, dish = get_test_dish

    response = await ac.get(list_path.format(menu.id, submenu.id))

    assert response.status_code == 200
    dishes = response.json()

    assert isinstance(dishes, list)
    assert len(dishes) == 1

    for dish in dishes:
        assert dish["id"] and UUID(dish["id"], version=4)
        assert isinstance(dish["title"], str)
        assert isinstance(dish["description"], str)
        assert isinstance(dish["price"], str)


@pytest.mark.asyncio
async def test_get_specific_dish(ac: AsyncClient, get_test_dish):
    """GET - тест получения определенного блюда"""
    menu, submenu, dish = get_test_dish

    response = await ac.get(detail_path.format(menu.id, submenu.id, dish.id))

    assert response.status_code == 200

    dish = response.json()

    assert dish["id"] and UUID(dish["id"], version=4)
    assert isinstance(dish["title"], str) and dish["title"] == "d title"
    assert (
        isinstance(dish["description"], str) and dish["description"] == "d description"
    )
    assert isinstance(dish["price"], str) and dish["price"] == "99.99"


@pytest.mark.asyncio
async def test_get_specific_dish_fail(ac: AsyncClient, get_test_submenu):
    """GET - тест получения несуществующего/некорректного блюда"""
    menu, submenu = get_test_submenu

    invalid_id = "fr fax"
    response = await ac.get(detail_path.format(menu.id, submenu.id, invalid_id))
    assert response.status_code == 422

    fake_id = uuid4()
    response = await ac.get(detail_path.format(menu.id, submenu.id, fake_id))
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_dish(ac: AsyncClient, get_test_submenu):
    """POST - тест создания блюда"""
    menu, submenu = get_test_submenu

    dish_data = {"title": "d title", "description": "d description", "price": 99.99}
    response = await ac.post(list_path.format(menu.id, submenu.id), json=dish_data)
    dish = response.json()

    assert response.status_code == 201

    assert dish["id"] and UUID(dish["id"], version=4)
    assert isinstance(dish["title"], str) and dish["title"] == "d title"
    assert (
        isinstance(dish["description"], str) and dish["description"] == "d description"
    )
    assert isinstance(dish["price"], str) and dish["price"] == "99.99"


@pytest.mark.asyncio
async def test_create_dish_fail(ac: AsyncClient, get_test_submenu):
    """POST - тест создания блюда c некорректными данными"""
    menu, submenu = get_test_submenu

    invalid_data = {"title": "d title", "description": 12, "price": "da price"}
    response = await ac.post(list_path.format(menu.id, submenu.id), json=invalid_data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_dish(ac: AsyncClient, get_test_dish):
    """PATCH - тест обновления определенного блюда"""
    menu, submenu, dish = get_test_dish

    new_data = {"price": 23.23}
    response = await ac.patch(
        detail_path.format(menu.id, submenu.id, dish.id), json=new_data
    )

    assert response.status_code == 200

    dish = response.json()

    assert dish["id"] and UUID(dish["id"], version=4)
    assert isinstance(dish["title"], str) and dish["title"] == "d title"
    assert (
        isinstance(dish["description"], str) and dish["description"] == "d description"
    )
    assert isinstance(dish["price"], str) and dish["price"] == "23.23"


@pytest.mark.asyncio
async def test_update_dish_fail(ac: AsyncClient, get_test_dish):
    """PATCH - тест обновления определенного блюда c некорректными данными"""
    menu, submenu, dish = get_test_dish

    invalid_data = {"price": "sewy"}
    response = await ac.patch(
        detail_path.format(menu.id, submenu.id, dish.id), json=invalid_data
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_dish(ac: AsyncClient, get_test_dish):
    """DELETE - тест удаления определенного блюда"""
    menu, submenu, dish = get_test_dish

    response = await ac.delete(detail_path.format(menu.id, submenu.id, dish.id))
    assert response.status_code == 200

    response = await ac.get(detail_path.format(menu.id, submenu.id, dish.id))
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_dish_fail(ac: AsyncClient, get_test_submenu):
    """DELETE - тест удаления несуществующего/некорректного блюда"""
    menu, submenu = get_test_submenu

    invalid_id = "invalid_id"
    response = await ac.delete(detail_path.format(menu.id, submenu.id, invalid_id))
    assert response.status_code == 422

    fake_id = uuid4()
    response = await ac.delete(detail_path.format(menu.id, submenu.id, fake_id))
    assert response.status_code == 404
