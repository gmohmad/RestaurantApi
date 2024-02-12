from uuid import UUID

from src.api.dish.crud_repo import DishCRUDRepo
from src.api.menu.crud_repo import MenuCRUDRepo
from src.api.submenu.crud_repo import SubMenuCRUDRepo
from src.database import async_session_maker, get_redis
from src.schemas.dish_schemas import DishInput, DishUpdate
from src.schemas.menu_schemas import MenuInput, MenuUpdate
from src.schemas.submenu_schemas import SubMenuInput, SubMenuUpdate


class SynchronizerRepo:
    def __init__(self, parsed_data: list[dict]) -> None:
        self.redis = get_redis()
        self.parsed_data = parsed_data

    async def initialize_repos(self) -> None:
        """Инициализация CRUD репозиториев"""
        async with async_session_maker() as session:
            self.menu_repo = MenuCRUDRepo(session)
            self.submenu_repo = SubMenuCRUDRepo(session)
            self.dish_repo = DishCRUDRepo(session)

    async def create_submenus(self, menu_id: UUID, submenus: list) -> None:
        """Добавление нескольких подменю"""
        for submenu in submenus:
            await self.submenu_repo.create_submenu(menu_id, SubMenuInput(**submenu))

    async def create_dishes(
        self,
        submenu_id: UUID,
        dishes: list,
    ) -> None:
        """Добавление нескольких блюд"""
        for dish in dishes:
            await self.dish_repo.create_dish(submenu_id, DishInput(**dish))

    async def sync_menu(self, menu: dict) -> None:
        """Синхронизвция определенного меню"""
        db_menu = await self.menu_repo.get_specific_menu(menu['id'])
        menu_copy = menu.copy()
        del menu_copy['id']
        if db_menu.title != menu['title'] or db_menu.description != menu['description']:
            await self.menu_repo.update_menu(menu['id'], MenuUpdate(**menu_copy))

    async def sync_submenu(self, menu_id: UUID, submenu: dict) -> None:
        """Синхронизвция определенного подменю"""
        db_submenu = await self.submenu_repo.get_specific_submenu(
            menu_id, submenu['id']
        )
        submenu_copy = submenu.copy()
        del submenu_copy['id']
        if (
            db_submenu.title != submenu['title']
            or db_submenu.description != submenu['description']
        ):
            await self.submenu_repo.update_submenu(
                menu_id, submenu['id'], SubMenuUpdate(**submenu_copy)
            )

    async def sync_dish(self, menu_id: UUID, submenu_id: UUID, dish: dict) -> None:
        """Синхронизвция определенного блюда"""
        db_dish = await self.dish_repo.get_specific_dish(
            menu_id, submenu_id, dish['id']
        )

        dish_copy = dish.copy()
        del dish_copy['id']
        if (
            db_dish.title != dish['title']
            or db_dish.description != dish['description']
            or db_dish.price != dish['price']
            or db_dish.discount != dish['discount']
        ):
            await self.dish_repo.update_dish(
                menu_id, submenu_id, dish['id'], DishUpdate(**dish_copy)
            )

    async def sync_dishes(self, menu_id: UUID, submenu_id: UUID, dishes: list) -> None:
        """Синхронизвция всех блюд"""
        dish_ids = [
            str(dish.id) for dish in await self.dish_repo.get_all_dishes(submenu_id)
        ]
        for dish in dishes:
            if dish['id'] not in dish_ids:
                await self.dish_repo.create_dish(submenu_id, DishInput(**dish))
            else:
                await self.sync_dish(menu_id, submenu_id, dish)
                dish_ids.remove(dish['id'])
        for id in dish_ids:
            await self.dish_repo.delete_dish(menu_id, submenu_id, UUID(id))

    async def sync_submenus(self, menu_id: UUID, submenus: list) -> None:
        """Синхронизвция всех подменю"""
        submenu_ids = [
            str(submenu.id)
            for submenu in await self.submenu_repo.get_all_submenus(menu_id)
        ]
        for submenu in submenus:
            if submenu['id'] not in submenu_ids:
                await self.submenu_repo.create_submenu(menu_id, SubMenuInput(**submenu))
                await self.create_dishes(submenu['id'], submenu['dishes'])
            else:
                await self.sync_submenu(menu_id, submenu)
                if submenu['dishes']:
                    await self.sync_dishes(menu_id, submenu['id'], submenu['dishes'])
                submenu_ids.remove(submenu['id'])
        for id in submenu_ids:
            await self.submenu_repo.delete_submenu(menu_id, UUID(id))

    async def sync_menus(self) -> None:
        """Синхронизвция всех меню"""
        menu_ids = [str(menu.id) for menu in await self.menu_repo.get_all_menus()]
        for menu in self.parsed_data:
            if menu['id'] not in menu_ids:
                await self.menu_repo.create_menu(MenuInput(**menu))
                await self.create_submenus(menu['id'], menu['submenus'])
                for submenu in menu['submenus']:
                    await self.create_dishes(submenu['id'], submenu['dishes'])
            else:
                await self.sync_menu(menu)
                if menu['submenus']:
                    await self.sync_submenus(menu['id'], menu['submenus'])
                menu_ids.remove(menu['id'])

        for id in menu_ids:
            await self.menu_repo.delete_menu(UUID(id))

    async def run_synchronization(self) -> None:
        """Запуск синхронизации"""
        await self.initialize_repos()
        await self.sync_menus()
        await self.redis.flushall()
