from uuid import UUID

from httpx import AsyncClient

from tests.reverse import reverse


async def test_create_menu_postman(ac: AsyncClient, ids_storage: dict[str, str]):
    """POST - Создает меню"""
    menu_data = {'title': 'm title', 'description': 'm description'}
    response = await ac.post(reverse('create_menu'), json=menu_data)
    assert response.status_code == 201
    menu = response.json()

    assert menu['id'] and UUID(menu['id'], version=4)
    assert menu['title'] == 'm title'
    assert menu['description'] == 'm description'
    assert menu['submenus_count'] == 0
    assert menu['dishes_count'] == 0

    ids_storage['menu_id'] = menu['id']


async def test_create_submenu_postman(ac: AsyncClient, ids_storage: dict[str, str]):
    """POST - Создает подменю"""
    submenu_data = {'title': 'sm title', 'description': 'sm description'}
    response = await ac.post(
        reverse('create_submenu', target_menu_id=ids_storage['menu_id']),
        json=submenu_data,
    )
    assert response.status_code == 201
    submenu = response.json()

    assert submenu['id'] and UUID(submenu['id'], version=4)
    assert submenu['title'] == 'sm title'
    assert submenu['description'] == 'sm description'
    assert submenu['dishes_count'] == 0

    ids_storage['submenu_id'] = submenu['id']


async def test_create_dish1_postman(ac: AsyncClient, ids_storage: dict[str, str]):
    """POST - Создает блюдо 1"""
    dish_data = {'title': 'd1 title', 'description': 'd1 description', 'price': 34.99}
    response = await ac.post(
        reverse(
            'create_dish',
            target_menu_id=ids_storage['menu_id'],
            target_submenu_id=ids_storage['submenu_id'],
        ),
        json=dish_data,
    )
    assert response.status_code == 201
    dish = response.json()

    assert dish['id'] and UUID(dish['id'], version=4)
    assert dish['title'] == 'd1 title'
    assert dish['description'] == 'd1 description'
    assert dish['price'] == '34.99'


async def test_create_dish2_postman(ac: AsyncClient, ids_storage: dict[str, str]):
    """POST - Создает блюдо 2"""
    dish_data = {'title': 'd2 title', 'description': 'd2 description', 'price': 35.99}
    response = await ac.post(
        reverse(
            'create_dish',
            target_menu_id=ids_storage['menu_id'],
            target_submenu_id=ids_storage['submenu_id'],
        ),
        json=dish_data,
    )
    assert response.status_code == 201
    dish = response.json()

    assert dish['id'] and UUID(dish['id'], version=4)
    assert dish['title'] == 'd2 title'
    assert dish['description'] == 'd2 description'
    assert dish['price'] == '35.99'


async def test_get_specific_menu_postman(ac: AsyncClient, ids_storage: dict[str, str]):
    """GET - просматривает определенное меню"""
    response = await ac.get(reverse('get_menu', target_menu_id=ids_storage['menu_id']))
    assert response.status_code == 200

    menu = response.json()

    assert menu['id'] and UUID(menu['id'], version=4)
    assert menu['title'] == 'm title'
    assert menu['description'] == 'm description'
    assert menu['submenus_count'] == 1
    assert menu['dishes_count'] == 2


async def test_get_specific_submenu_postman(
    ac: AsyncClient, ids_storage: dict[str, str]
):
    """GET - просматривает определенное подменю"""
    response = await ac.get(
        reverse(
            'get_submenu',
            target_menu_id=ids_storage['menu_id'],
            target_submenu_id=ids_storage['submenu_id'],
        )
    )
    assert response.status_code == 200
    submenu = response.json()

    assert submenu['id'] and UUID(submenu['id'], version=4)
    assert submenu['title'] == 'sm title'
    assert submenu['description'] == 'sm description'
    assert submenu['dishes_count'] == 2


async def test_delete_submenu_postman(ac: AsyncClient, ids_storage: dict[str, str]):
    """DELETE - Удаляет подменю"""
    response = await ac.delete(
        reverse(
            'get_submenu',
            target_menu_id=ids_storage['menu_id'],
            target_submenu_id=ids_storage['submenu_id'],
        )
    )
    assert response.status_code == 200

    response = await ac.get(
        f"api/v1/menus/{ids_storage['menu_id']}/submenus/{ids_storage['submenu_id']}"
    )
    assert response.status_code == 404


async def test_get_all_submenus_postman(ac: AsyncClient, ids_storage: dict[str, str]):
    """GET - просматривает список подменю"""
    response = await ac.get(
        reverse('get_submenus', target_menu_id=ids_storage['menu_id'])
    )

    assert response.status_code == 200
    submenus = response.json()
    assert isinstance(submenus, list)
    assert submenus == []


async def test_get_all_dishes_postman(ac: AsyncClient, ids_storage: dict[str, str]):
    """GET - просматривает список блюд"""
    response = await ac.get(
        reverse(
            'get_dishes',
            target_menu_id=ids_storage['menu_id'],
            target_submenu_id=ids_storage['submenu_id'],
        )
    )
    assert response.status_code == 200
    dishes = response.json()
    assert isinstance(dishes, list)
    assert dishes == []


async def test_get_specific_menu_with_no_childs_postman(
    ac: AsyncClient, ids_storage: dict[str, str]
):
    """GET - просматривает определенное меню"""
    response = await ac.get(reverse('get_menu', target_menu_id=ids_storage['menu_id']))

    assert response.status_code == 200

    menu = response.json()

    assert menu['id'] and UUID(menu['id'], version=4)
    assert menu['title'] == 'm title'
    assert menu['description'] == 'm description'
    assert menu['submenus_count'] == 0
    assert menu['dishes_count'] == 0


async def test_delete_menu_postman(ac: AsyncClient, ids_storage: dict[str, str]):
    """DELETE - Удаляет меню"""
    response = await ac.delete(
        reverse('delete_menu', target_menu_id=ids_storage['menu_id'])
    )
    assert response.status_code == 200

    response = await ac.get(reverse('get_menu', target_menu_id=ids_storage['menu_id']))
    assert response.status_code == 404


async def test_get_all_menus_postman(ac: AsyncClient):
    """GET - просматривает список меню"""
    response = await ac.get(reverse('get_menus'))

    assert response.status_code == 200
    menus = response.json()
    assert isinstance(menus, list)
    assert menus == []
