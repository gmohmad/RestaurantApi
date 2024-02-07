from uuid import UUID

from fastapi import Depends

from src.api.submenu.crud_repo import SubMenuCRUDRepo
from src.caching.cache_repo import CacheRepo
from src.model_definitions.models import SubMenu
from src.schemas.submenu_schemas import SubMenuInput


class SubMenuServiceRepo:
    """Service репозиторий для меню"""

    def __init__(
        self,
        crud_repo: SubMenuCRUDRepo = Depends(),
        cache_repo: CacheRepo = Depends(),
    ) -> None:
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_all_submenus(self, menu_id: UUID) -> list[SubMenu]:
        """Получение всех подменю"""
        cache = await self.cache_repo.get_all_submenus_cache(menu_id)
        if cache:
            return cache
        submenus = await self.crud_repo.get_all_submenus(menu_id)
        await self.cache_repo.set_all_submenus_cache(menu_id, submenus)

        return submenus

    async def get_specific_submenu(self, menu_id: UUID, submenu_id: UUID) -> SubMenu:
        """Получение определенного подменю"""
        cache = await self.cache_repo.get_submenu_cache(menu_id, submenu_id)
        if cache:
            return cache
        submenu = await self.crud_repo.get_specific_submenu(menu_id, submenu_id)
        await self.cache_repo.set_submenu_cache(menu_id, submenu)

        return submenu

    async def create_submenu(self, menu_id: UUID, data: SubMenuInput) -> SubMenu:
        """Добавление нового подменю"""
        submenu = await self.crud_repo.create_submenu(menu_id, data)
        await self.cache_repo.delete_all_submenu_cache(menu_id)

        return submenu

    async def update_submenu(
        self, menu_id: UUID, submenu_id: UUID, data: SubMenuInput
    ) -> SubMenu:
        """Изменение подменю"""
        submenu = await self.crud_repo.update_submenu(menu_id, submenu_id, data)
        await self.cache_repo.delete_submenu_cache(menu_id, submenu_id)

        return submenu

    async def delete_submenu(self, menu_id: UUID, submenu_id: UUID) -> None:
        """Удаление подменю"""
        await self.crud_repo.delete_submenu(menu_id, submenu_id)

        await self.cache_repo.delete_all_submenu_cache(menu_id)
        await self.cache_repo.delete_submenu_cache(menu_id, submenu_id)
        await self.cache_repo.delete_submenu_tree_cache(menu_id, submenu_id)
