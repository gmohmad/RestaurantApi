import pytest
from uuid import UUID, uuid4
from httpx import AsyncClient
from fastapi import HTTPException
from decimal import Decimal

from src.models.models import Dish
from src.utils import get_dish_by_id
from tests.conftest import async_session_maker
from tests.fixtures import prepare_database


list_path = "api/v1/menus/{}/submenus/{}/dishes/"
detail_path = "api/v1/menus/{}/submenus/{}/dishes/{}"


@pytest.mark.asyncio
async def test_get_all_dishes_empty(ac: AsyncClient, get_test_submenu):
    """GET - тест получения всех блюд, когда нет ни одного блюда"""
    new_menu, new_submenu = get_test_submenu

    response = await ac.get(list_path.format(new_menu.id, new_submenu.id))

    assert response.status_code == 200
    dishes = response.json()

    assert isinstance(dishes, list)
    assert dishes == []


@pytest.mark.asyncio
async def test_get_all_dishes(ac: AsyncClient, get_test_dish):
    """GET - тест получения всех блюд"""
    new_menu, new_submenu, new_dish = get_test_dish

    response = await ac.get(list_path.format(new_menu.id, new_submenu.id))

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
    new_menu, new_submenu, new_dish = get_test_dish

    response = await ac.get(detail_path.format(new_menu.id, new_submenu.id, new_dish.id))

    assert response.status_code == 200

    dish = response.json()

    assert dish["id"] == str(new_dish.id)
    assert dish["title"] == "d title"
    assert dish["description"] == "d description"
    assert dish["price"] == "99.99"


@pytest.mark.asyncio
async def test_get_specific_dish_fail(ac: AsyncClient, get_test_submenu):
    """GET - тест получения несуществующего/некорректного блюда"""
    new_menu, new_submenu = get_test_submenu

    invalid_id = "fr fax"
    response = await ac.get(detail_path.format(new_menu.id, new_submenu.id, invalid_id))
    assert response.status_code == 422

    fake_id = uuid4()
    response = await ac.get(detail_path.format(new_menu.id, new_submenu.id, fake_id))
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_dish(ac: AsyncClient, get_test_submenu):
    """POST - тест создания блюда"""
    new_menu, new_submenu = get_test_submenu

    dish_data = {"title": "d title", "description": "d description", "price": 99.99}
    response = await ac.post(list_path.format(new_menu.id, new_submenu.id), json=dish_data)
    dish = response.json()

    assert response.status_code == 201

    assert dish["id"] and UUID(dish["id"], version=4)
    assert dish["title"] == dish_data["title"]
    assert dish["description"] == dish_data["description"]
    assert dish["price"] == str(dish_data["price"])

    async with async_session_maker() as session:
        db_dish = await get_dish_by_id(new_menu.id, new_submenu.id, dish["id"], session)

        assert isinstance(db_dish, Dish)
        assert db_dish.id == UUID(dish["id"])
        assert db_dish.title == dish_data["title"]
        assert db_dish.description == dish_data["description"]
        assert db_dish.price == round(Decimal(dish_data["price"]), 2)


@pytest.mark.asyncio
async def test_create_dish_fail(ac: AsyncClient, get_test_submenu):
    """POST - тест создания блюда c некорректными данными"""
    new_menu, new_submenu = get_test_submenu

    invalid_data = {"title": "d title", "description": 12, "price": "da price"}
    response = await ac.post(list_path.format(new_menu.id, new_submenu.id), json=invalid_data)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_dish(ac: AsyncClient, get_test_dish):
    """PATCH - тест обновления определенного блюда"""
    new_menu, new_submenu, new_dish = get_test_dish

    new_dish_data = {"price": 23.23}
    response = await ac.patch(
        detail_path.format(new_menu.id, new_submenu.id, new_dish.id), json=new_dish_data
    )
    assert response.status_code == 200
    dish = response.json()

    assert dish["id"] == str(new_dish.id)
    assert dish["title"] == "d title"
    assert dish["description"] == "d description"
    assert dish["price"] == str(new_dish_data["price"])

    async with async_session_maker() as session:
        db_dish = await get_dish_by_id(new_menu.id, new_submenu.id, dish["id"], session)

        assert isinstance(db_dish, Dish)
        assert db_dish.id == UUID(dish["id"])
        assert db_dish.title == "d title"
        assert db_dish.description == "d description"
        assert db_dish.price == round(Decimal(new_dish_data["price"]), 2)


@pytest.mark.asyncio
async def test_update_dish_fail(ac: AsyncClient, get_test_dish):
    """PATCH - тест обновления определенного блюда c некорректными данными"""
    new_menu, new_submenu, new_dish = get_test_dish

    invalid_data = {"price": "sewy"}
    response = await ac.patch(
        detail_path.format(new_menu.id, new_submenu.id, new_dish.id), json=invalid_data
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_dish(ac: AsyncClient, get_test_dish):
    """DELETE - тест удаления определенного блюда"""
    new_menu, new_submenu, new_dish = get_test_dish

    response = await ac.delete(detail_path.format(new_menu.id, new_submenu.id, new_dish.id))
    assert response.status_code == 200

    with pytest.raises(HTTPException) as exc_info:
        async with async_session_maker() as session:
            await get_dish_by_id(new_menu.id, new_submenu.id, new_dish.id, session)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "dish not found"


@pytest.mark.asyncio
async def test_delete_dish_fail(ac: AsyncClient, get_test_submenu):
    """DELETE - тест удаления несуществующего/некорректного блюда"""
    new_menu, new_submenu = get_test_submenu

    invalid_id = "invalid_id"
    response = await ac.delete(detail_path.format(new_menu.id, new_submenu.id, invalid_id))
    assert response.status_code == 422

    fake_id = uuid4()
    response = await ac.delete(detail_path.format(new_menu.id, new_submenu.id, fake_id))
    assert response.status_code == 404
