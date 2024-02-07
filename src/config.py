import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'

MENUS_TREE = '/menus-tree/'
MENUS_URL = '/menus/'
MENU_URL = '/menus/{target_menu_id}'
SUBMENUS_URL = '/menus/{target_menu_id}/submenus/'
SUBMENU_URL = '/menus/{target_menu_id}/submenus/{target_submenu_id}'
DISHES_URL = '/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/'
DISH_URL = (
    '/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
)
