from uuid import UUID, uuid4

import pytest
from fastapi import HTTPException
from httpx import AsyncClient

from src.model_definitions.models import Menu
from src.utils import get_menu_by_id
from tests.conftest import SessionMaker
from tests.reverse import reverse


async def test_get_all_menus_empty(ac: AsyncClient):
    """GET - тест получения всех меню, когда нет ни одного меню"""
    response = await ac.get(reverse('get_menus'))

    assert response.status_code == 200
    menus = response.json()
    assert isinstance(menus, list)
    assert menus == []


async def test_create_menu(ac: AsyncClient, ids_storage: dict[str, str]):
    """POST - тест создания меню"""
    menu_data = {'title': 'm title', 'description': 'm description'}
    response = await ac.post(reverse('create_menu'), json=menu_data)

    assert response.status_code == 201

    menu = response.json()

    assert menu['id'] and UUID(menu['id'], version=4)
    assert menu['title'] == menu_data['title']
    assert menu['description'] == menu_data['description']
    assert menu['submenus_count'] == 0
    assert menu['dishes_count'] == 0

    async with SessionMaker() as session:
        db_menu = await get_menu_by_id(menu['id'], session)

        assert isinstance(db_menu, Menu)
        assert db_menu.id == UUID(menu['id'])
        assert db_menu.title == menu_data['title']
        assert db_menu.description == menu_data['description']
        assert db_menu.submenus_count == 0
        assert db_menu.dishes_count == 0

    ids_storage['menu_id'] = menu['id']


async def test_create_menu_fail(ac: AsyncClient):
    """POST - тест создания меню с некорректными данными"""
    invalid_data = {'title': 12, 'description': None}
    response = await ac.post(reverse('create_menu'), json=invalid_data)

    assert response.status_code == 422


async def test_get_all_menus(ac: AsyncClient):
    """GET - тест получения всех меню"""
    response = await ac.get(reverse('get_menus'))

    assert response.status_code == 200
    menus = response.json()

    assert isinstance(menus, list)
    assert len(menus) == 1

    for menu in menus:
        assert menu['id'] and UUID(menu['id'], version=4)
        assert isinstance(menu['title'], str)
        assert isinstance(menu['description'], str)
        assert isinstance(menu['submenus_count'], int)
        assert isinstance(menu['dishes_count'], int)


async def test_get_specific_menu(ac: AsyncClient, ids_storage: dict[str, str]):
    """GET - тест получения определенного меню"""
    response = await ac.get(reverse('get_menu', target_menu_id=ids_storage['menu_id']))
    assert response.status_code == 200

    menu = response.json()

    assert menu['id'] == ids_storage['menu_id']
    assert menu['title'] == 'm title'
    assert menu['description'] == 'm description'
    assert menu['submenus_count'] == 0
    assert menu['dishes_count'] == 0


async def test_get_specific_menu_fail(ac: AsyncClient):
    """GET - тест получения несуществующего/некорректного меню"""
    invalid_id = 'gotta get that internship'
    response = await ac.get(reverse('get_menu', target_menu_id=invalid_id))

    assert response.status_code == 422

    fake_id = str(uuid4())
    response = await ac.get(reverse('get_menu', target_menu_id=fake_id))

    assert response.status_code == 404


async def test_update_menu(ac: AsyncClient, ids_storage: dict[str, str]):
    """PATCH - тест обновления определенного меню"""
    new_menu_data = {'title': 'new title'}
    response = await ac.patch(
        reverse('update_menu', target_menu_id=ids_storage['menu_id']),
        json=new_menu_data,
    )
    assert response.status_code == 200

    menu = response.json()

    assert menu['id'] == ids_storage['menu_id']
    assert menu['title'] == new_menu_data['title']
    assert menu['description'] == 'm description'
    assert menu['submenus_count'] == 0
    assert menu['dishes_count'] == 0

    async with SessionMaker() as session:
        db_menu = await get_menu_by_id(menu['id'], session)

        assert isinstance(db_menu, Menu)
        assert db_menu.id == UUID(menu['id'])
        assert db_menu.title == new_menu_data['title']
        assert db_menu.description == 'm description'
        assert db_menu.submenus_count == 0
        assert db_menu.dishes_count == 0


async def test_update_menu_fail(ac: AsyncClient, ids_storage: dict[str, str]):
    """PATCH - тест обновления определенного меню c некорректными данными"""
    invalid_data = {'description': 12}
    response = await ac.patch(
        reverse('update_menu', target_menu_id=ids_storage['menu_id']), json=invalid_data
    )

    assert response.status_code == 422


async def test_delete_menu(ac: AsyncClient, ids_storage: dict[str, str]):
    """DELETE - тест удаления определенного меню"""
    response = await ac.delete(
        reverse('delete_menu', target_menu_id=ids_storage['menu_id'])
    )
    assert response.status_code == 200

    with pytest.raises(HTTPException) as exc_info:
        async with SessionMaker() as session:
            await get_menu_by_id(ids_storage['menu_id'], session)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == 'menu not found'


async def test_delete_menu_fail(ac: AsyncClient):
    """DELETE - тест удаления несуществующего/некорректного меню"""

    invalid_id = 'some random stuff'
    response = await ac.delete(reverse('delete_menu', target_menu_id=invalid_id))
    assert response.status_code == 422

    fake_id = str(uuid4())
    get_resp = await ac.delete(reverse('delete_menu', target_menu_id=fake_id))
    assert get_resp.status_code == 404
