from uuid import UUID

from fastapi import Depends

from src.api.dish.crud_repo import DishCRUDRepo
from src.caching.cache_repo import CacheRepo
from src.model_definitions.models import Dish
from src.schemas.dish_schemas import DishInput


class DishServiceRepo:
    """Service репозиторий для меню"""

    def __init__(
        self,
        crud_repo: DishCRUDRepo = Depends(),
        cache_repo: CacheRepo = Depends(),
    ) -> None:
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_all_dishes(self, menu_id: UUID, submenu_id: UUID) -> list[Dish]:
        """Получение всех блюд"""
        cache = await self.cache_repo.get_all_dishes_cache(menu_id, submenu_id)
        if cache:
            return cache
        dishes = await self.crud_repo.get_all_dishes(submenu_id)
        await self.cache_repo.set_all_dishes_cache(menu_id, submenu_id, dishes)

        return dishes

    async def get_specific_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> Dish:
        """Получение определенного блюда"""
        cache = await self.cache_repo.get_dish_cache(menu_id, submenu_id, dish_id)
        if cache:
            return cache
        dish = await self.crud_repo.get_specific_dish(menu_id, submenu_id, dish_id)
        await self.cache_repo.set_dish_cache(menu_id, submenu_id, dish)

        return dish

    async def create_dish(
        self, menu_id: UUID, submenu_id: UUID, data: DishInput
    ) -> Dish:
        """Добавление нового блюда"""
        dish = await self.crud_repo.create_dish(submenu_id, data)
        await self.cache_repo.delete_all_dishes_cache(menu_id, submenu_id)

        return dish

    async def update_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, data: DishInput
    ) -> Dish:
        """Изменение блюда"""
        dish = await self.crud_repo.update_dish(menu_id, submenu_id, dish_id, data)
        await self.cache_repo.delete_dish_cache(menu_id, submenu_id, dish_id)

        return dish

    async def delete_dish(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
        """Удаление блюда"""
        await self.crud_repo.delete_dish(menu_id, submenu_id, dish_id)
        await self.cache_repo.delete_all_dishes_cache(menu_id, submenu_id)
        await self.cache_repo.delete_dish_cache(menu_id, submenu_id, dish_id)
