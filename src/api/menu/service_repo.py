from fastapi import Depends
from typing import List
from uuid import UUID

from src.schemas.menu_schemas import MenuInput
from src.models.models import Menu
from src.cache_repo import CacheRepo
from src.api.menu.crud_repo import MenuCRUDRepo


class MenuServiceRepo:
    """Service репозиторий для меню"""

    def __init__(
        self, crud_repo: MenuCRUDRepo = Depends(), cache_repo: CacheRepo = Depends()
    ) -> None:
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_all_menus(self) -> List[Menu]:
        """Получение всех меню"""
        cache = await self.cache_repo.get_all_menus_cache()
        if cache:
            return cache
        menus = await self.crud_repo.get_all_menus()
        await self.cache_repo.set_all_menus_cache(menus)

        return menus

    async def get_specific_menu(self, menu_id: UUID) -> Menu:
        """Получение определенного меню"""
        cache = await self.cache_repo.get_menu_cache(menu_id)
        if cache:
            return cache
        menu = await self.crud_repo.get_specific_menu(menu_id)
        await self.cache_repo.set_menu_cache(menu)

        return menu

    async def create_menu(self, data: MenuInput) -> Menu:
        """Добавление нового меню"""
        menu = await self.crud_repo.create_menu(data)
        await self.cache_repo.delete_all_menu_cache()

        return menu

    async def update_menu(self, menu_id: UUID, data: MenuInput) -> Menu:
        """Изменение меню"""
        menu = await self.crud_repo.update_menu(menu_id, data)
        await self.cache_repo.delete_menu_cache(menu_id)

        return menu

    async def delete_menu(self, menu_id: UUID) -> None:
        """Удаление меню"""
        await self.crud_repo.delete_menu(menu_id)
        await self.cache_repo.delete_menu_cache(menu_id)
        await self.cache_repo.delete_menu_tree_cache(menu_id)
