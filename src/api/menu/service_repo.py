from uuid import UUID

from fastapi import BackgroundTasks, Depends

from src.api.menu.crud_repo import MenuCRUDRepo
from src.caching.cache_repo import CacheRepo
from src.model_definitions.models import Menu
from src.schemas.menu_schemas import MenuInput


class MenuServiceRepo:
    """Service репозиторий для меню"""

    def __init__(
        self, crud_repo: MenuCRUDRepo = Depends(), cache_repo: CacheRepo = Depends()
    ) -> None:
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_menus_tree(self, bg_tasks: BackgroundTasks) -> list[Menu]:
        """Получение всех меню с подменю и блюдами связанными с ними"""
        cache = await self.cache_repo.get_menus_tree_cache()
        if cache:
            return cache
        menus_tree = await self.crud_repo.get_menus_tree()
        bg_tasks.add_task(self.cache_repo.set_menus_tree_cache, menus_tree)

        return menus_tree

    async def get_all_menus(self, bg_tasks: BackgroundTasks) -> list[Menu]:
        """Получение всех меню"""
        cache = await self.cache_repo.get_all_menus_cache()
        if cache:
            return cache
        menus = await self.crud_repo.get_all_menus()
        bg_tasks.add_task(self.cache_repo.set_all_menus_cache, menus)

        return menus

    async def get_specific_menu(self, bg_tasks: BackgroundTasks, menu_id: UUID) -> Menu:
        """Получение определенного меню"""
        cache = await self.cache_repo.get_menu_cache(menu_id)
        if cache:
            return cache
        menu = await self.crud_repo.get_specific_menu(menu_id)
        bg_tasks.add_task(self.cache_repo.set_menu_cache, menu)

        return menu

    async def create_menu(self, bg_tasks: BackgroundTasks, data: MenuInput) -> Menu:
        """Добавление нового меню"""
        menu = await self.crud_repo.create_menu(data)
        bg_tasks.add_task(self.cache_repo.delete_all_menu_cache)
        bg_tasks.add_task(self.cache_repo.delete_menus_tree_cache)

        return menu

    async def update_menu(
        self, bg_tasks: BackgroundTasks, menu_id: UUID, data: MenuInput
    ) -> Menu:
        """Изменение меню"""
        menu = await self.crud_repo.update_menu(menu_id, data)
        bg_tasks.add_task(self.cache_repo.delete_menu_cache, menu_id)
        bg_tasks.add_task(self.cache_repo.delete_menus_tree_cache)

        return menu

    async def delete_menu(self, bg_tasks: BackgroundTasks, menu_id: UUID) -> None:
        """Удаление меню"""
        await self.crud_repo.delete_menu(menu_id)
        bg_tasks.add_task(self.cache_repo.delete_menu_cache, menu_id)
        bg_tasks.add_task(self.cache_repo.delete_menu_tree_cache, menu_id)
        bg_tasks.add_task(self.cache_repo.delete_menus_tree_cache)
