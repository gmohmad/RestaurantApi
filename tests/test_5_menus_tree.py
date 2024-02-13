from uuid import UUID

from httpx import AsyncClient

from tests.reverse import reverse


async def test_menus_tree_empty(ac: AsyncClient, restore_database):
    """GET - тест эндпойнта get_menus_tree, когда нет ни одного меню"""
    response = await ac.get(reverse('get_menus_tree'))
    assert response.status_code == 200
    menus_tree = response.json()
    assert isinstance(menus_tree, list)
    assert menus_tree == []


async def test_create_menu(ac: AsyncClient, ids_storage: dict[str, str]):
    """POST - тест создания меню"""
    menu_data = {'title': 'm title', 'description': 'm description'}
    response = await ac.post(reverse('create_menu'), json=menu_data)
    assert response.status_code == 201
    ids_storage['menu_id'] = response.json()['id']


async def test_menus_tree_with_one_menu(ac: AsyncClient):
    """GET - тест эндпойнта get_menus_tree с одним меню"""
    response = await ac.get(reverse('get_menus_tree'))
    assert response.status_code == 200
    menus_tree = response.json()
    assert isinstance(menus_tree, list)
    assert len(menus_tree) == 1

    menu = menus_tree[0]
    assert menu['id'] and UUID(menu['id'], version=4)
    assert menu['title'] == 'm title'
    assert menu['description'] == 'm description'
    assert menu['submenus_count'] == 0
    assert menu['dishes_count'] == 0
    assert menu['submenus'] == []


async def test_create_submenu(ac: AsyncClient, ids_storage: dict[str, str]):
    """POST - тест создания подменю"""
    submenu_data = {'title': 'sm title', 'description': 'sm description'}
    response = await ac.post(
        reverse('create_submenu', target_menu_id=ids_storage['menu_id']),
        json=submenu_data,
    )
    assert response.status_code == 201
    ids_storage['submenu_id'] = response.json()['id']


async def test_menus_tree_with_one_submenu(ac: AsyncClient):
    """GET - тест эндпойнта get_menus_tree с одним подменю"""
    response = await ac.get(reverse('get_menus_tree'))
    assert response.status_code == 200
    menus_tree = response.json()
    assert isinstance(menus_tree, list)

    submenus = menus_tree[0]['submenus']
    assert len(submenus) == 1

    submenu = submenus[0]
    assert submenu != []
    assert submenu['id'] and UUID(submenu['id'], version=4)
    assert submenu['title'] == 'sm title'
    assert submenu['description'] == 'sm description'
    assert submenu['dishes_count'] == 0
    assert submenu['dishes'] == []


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
    }
    response = await ac.post(reverse('create_dish', **path_params), json=dish_data)

    assert response.status_code == 201


async def test_menus_tree_with_one_dish(ac: AsyncClient):
    """GET - тест эндпойнта get_menus_tree с одним блюдом"""
    response = await ac.get(reverse('get_menus_tree'))
    assert response.status_code == 200
    menus_tree = response.json()
    assert isinstance(menus_tree, list)

    dishes = menus_tree[0]['submenus'][0]['dishes']
    assert len(dishes) == 1

    dish = dishes[0]
    assert dish != []
    assert dish['id'] and UUID(dish['id'], version=4)
    assert dish['title'] == 'd title'
    assert dish['description'] == 'd description'
    assert dish['price'] == str(float(100))
