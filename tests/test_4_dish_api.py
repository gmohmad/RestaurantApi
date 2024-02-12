from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException
from httpx import AsyncClient

from src.model_definitions.models import Dish
from src.utils import get_dish_by_id
from tests.conftest import SessionMaker
from tests.reverse import reverse


async def test_create_menu(ac: AsyncClient, ids_storage: dict[str, str]):
    """POST - тест создания меню"""
    menu_data = {'title': 'm title', 'description': 'm description'}
    response = await ac.post(reverse('create_menu'), json=menu_data)
    assert response.status_code == 201
    ids_storage['menu_id'] = str(response.json()['id'])


async def test_create_submenu(ac: AsyncClient, ids_storage: dict[str, str]):
    """POST - тест создания подменю"""
    submenu_data = {'title': 'sm title', 'description': 'sm description'}
    response = await ac.post(
        reverse('create_submenu', target_menu_id=ids_storage['menu_id']),
        json=submenu_data,
    )
    assert response.status_code == 201
    ids_storage['submenu_id'] = str(response.json()['id'])


async def test_get_all_dishes_empty(ac: AsyncClient, ids_storage: dict[str, str]):
    """GET - тест получения всех блюд, когда нет ни одного блюда"""
    path_params = {
        'target_menu_id': ids_storage['menu_id'],
        'target_submenu_id': ids_storage['submenu_id'],
    }
    response = await ac.get(reverse('get_dishes', **path_params))

    assert response.status_code == 200
    dishes = response.json()

    assert isinstance(dishes, list)
    assert dishes == []


async def test_create_dish(ac: AsyncClient, ids_storage: dict[str, str]):
    """POST - тест создания блюда"""
    path_params = {
        'target_menu_id': ids_storage['menu_id'],
        'target_submenu_id': ids_storage['submenu_id'],
    }
    dish_data = {
        'title': 'd title',
        'description': 'd description',
        'price': 100,
        'discount': 20,
    }
    response = await ac.post(reverse('create_dish', **path_params), json=dish_data)
    dish = response.json()

    assert response.status_code == 201

    assert dish['id'] and UUID(dish['id'], version=4)
    assert dish['title'] == dish_data['title']
    assert dish['description'] == dish_data['description']

    assert dish['discount'] == 20
    price = float(str(dish_data['price']))
    discounted_price = float(price - (price * (dish['discount'] / 100)))
    assert dish['price'] == str(discounted_price)

    async with SessionMaker() as session:
        db_dish = await get_dish_by_id(
            ids_storage['menu_id'], ids_storage['submenu_id'], dish['id'], session
        )
        assert isinstance(db_dish, Dish)
        assert db_dish.id == UUID(dish['id'])
        assert db_dish.title == dish_data['title']
        assert db_dish.description == dish_data['description']
        assert db_dish.discount == dish_data['discount']
        assert db_dish.price == round(Decimal(str(dish_data['price'])), 2)
    ids_storage['dish_id'] = dish['id']


async def test_get_all_dishes(ac: AsyncClient, ids_storage: dict[str, str]):
    """GET - тест получения всех блюд"""
    path_params = {
        'target_menu_id': ids_storage['menu_id'],
        'target_submenu_id': ids_storage['submenu_id'],
    }
    response = await ac.get(reverse('get_dishes', **path_params))

    assert response.status_code == 200
    dishes = response.json()

    assert isinstance(dishes, list)
    assert len(dishes) == 1

    for dish in dishes:
        assert dish['id'] and UUID(dish['id'], version=4)
        assert isinstance(dish['title'], str)
        assert isinstance(dish['description'], str)
        assert isinstance(dish['price'], str)
        assert isinstance(dish['discount'], int)


async def test_get_specific_dish(ac: AsyncClient, ids_storage: dict[str, str]):
    """GET - тест получения определенного блюда"""
    path_params = {
        'target_menu_id': ids_storage['menu_id'],
        'target_submenu_id': ids_storage['submenu_id'],
        'target_dish_id': ids_storage['dish_id'],
    }
    response = await ac.get(reverse('get_dish', **path_params))

    assert response.status_code == 200

    dish = response.json()

    assert dish['id'] == ids_storage['dish_id']
    assert dish['title'] == 'd title'
    assert dish['description'] == 'd description'
    assert dish['discount'] == 20
    assert dish['price'] == str(float(80))


async def test_get_specific_dish_fail(ac: AsyncClient, ids_storage: dict[str, str]):
    """GET - тест получения несуществующего/некорректного блюда"""
    invalid_id = 'fr fax'
    response = await ac.get(
        reverse(
            'get_dish',
            target_menu_id=ids_storage['menu_id'],
            target_submenu_id=ids_storage['submenu_id'],
            target_dish_id=invalid_id,
        )
    )
    assert response.status_code == 422

    fake_id = str(uuid4())
    response = await ac.get(
        reverse(
            'get_dish',
            target_menu_id=ids_storage['menu_id'],
            target_submenu_id=ids_storage['submenu_id'],
            target_dish_id=fake_id,
        )
    )
    assert response.status_code == 404


async def test_create_dish_fail(ac: AsyncClient, ids_storage: dict[str, str]):
    """POST - тест создания блюда c некорректными данными"""
    path_params = {
        'target_menu_id': ids_storage['menu_id'],
        'target_submenu_id': ids_storage['submenu_id'],
        'target_dish_id': ids_storage['dish_id'],
    }
    invalid_data = {'title': 'd title', 'description': 12, 'price': 'da price'}
    response = await ac.post(reverse('create_dish', **path_params), json=invalid_data)
    assert response.status_code == 422


async def test_update_dish(ac: AsyncClient, ids_storage: dict[str, str]):
    """PATCH - тест обновления определенного блюда"""
    path_params = {
        'target_menu_id': ids_storage['menu_id'],
        'target_submenu_id': ids_storage['submenu_id'],
        'target_dish_id': ids_storage['dish_id'],
    }
    new_dish_data = {'price': 80}
    response = await ac.patch(reverse('update_dish', **path_params), json=new_dish_data)
    assert response.status_code == 200
    dish = response.json()

    assert dish['id'] == ids_storage['dish_id']
    assert dish['title'] == 'd title'
    assert dish['description'] == 'd description'
    assert dish['discount'] == 20
    assert dish['price'] == str(float(64))

    async with SessionMaker() as session:
        db_dish = await get_dish_by_id(
            ids_storage['menu_id'], ids_storage['submenu_id'], dish['id'], session
        )

        assert isinstance(db_dish, Dish)
        assert db_dish.id == UUID(dish['id'])
        assert db_dish.title == 'd title'
        assert db_dish.description == 'd description'
        assert db_dish.discount == 20
        assert db_dish.price == round(Decimal(new_dish_data['price']), 2)


async def test_update_dish_fail(ac: AsyncClient, ids_storage: dict[str, str]):
    """PATCH - тест обновления определенного блюда c некорректными данными"""
    path_params = {
        'target_menu_id': ids_storage['menu_id'],
        'target_submenu_id': ids_storage['submenu_id'],
        'target_dish_id': ids_storage['dish_id'],
    }
    invalid_data = {'price': 'sewy'}
    response = await ac.patch(reverse('update_dish', **path_params), json=invalid_data)

    assert response.status_code == 422


async def test_delete_dish(ac: AsyncClient, ids_storage: dict[str, str]):
    """DELETE - тест удаления определенного блюда"""
    path_params = {
        'target_menu_id': ids_storage['menu_id'],
        'target_submenu_id': ids_storage['submenu_id'],
        'target_dish_id': ids_storage['dish_id'],
    }
    response = await ac.delete(reverse('delete_dish', **path_params))
    assert response.status_code == 200

    with pytest.raises(HTTPException) as exc_info:
        async with SessionMaker() as session:
            await get_dish_by_id(
                ids_storage['menu_id'],
                ids_storage['submenu_id'],
                ids_storage['dish_id'],
                session,
            )

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == 'dish not found'


async def test_delete_dish_fail(ac: AsyncClient, ids_storage: dict[str, str]):
    """DELETE - тест удаления несуществующего/некорректного блюда"""
    invalid_id = 'invalid_id'
    response = await ac.delete(
        reverse(
            'delete_dish',
            target_menu_id=ids_storage['menu_id'],
            target_submenu_id=ids_storage['submenu_id'],
            target_dish_id=invalid_id,
        )
    )
    assert response.status_code == 422
    fake_id = str(uuid4())
    response = await ac.delete(
        reverse(
            'delete_dish',
            target_menu_id=ids_storage['menu_id'],
            target_submenu_id=ids_storage['submenu_id'],
            target_dish_id=fake_id,
        )
    )
    assert response.status_code == 404
