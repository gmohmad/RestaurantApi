from uuid import UUID

from fastapi import BackgroundTasks, Depends

from src.api.dish.crud_repo import DishCRUDRepo
from src.caching.cache_repo import CacheRepo
from src.model_definitions.models import Dish
from src.schemas.dish_schemas import DishInput
from src.utils import update_dish_price


class DishServiceRepo:
    """Service репозиторий для меню"""

    def __init__(
        self,
        crud_repo: DishCRUDRepo = Depends(),
        cache_repo: CacheRepo = Depends(),
    ) -> None:
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_all_dishes(
        self, bg_tasks: BackgroundTasks, menu_id: UUID, submenu_id: UUID
    ) -> list[Dish]:
        """Получение всех блюд"""
        cache = await self.cache_repo.get_all_dishes_cache(menu_id, submenu_id)
        if cache:
            return cache
        dishes = await self.crud_repo.get_all_dishes(submenu_id)

        for dish in dishes:
            discount = await self.cache_repo.get_discount_cache(dish.id)
            update_dish_price(dish, discount)

        bg_tasks.add_task(
            self.cache_repo.set_all_dishes_cache, menu_id, submenu_id, dishes
        )

        return dishes

    async def get_specific_dish(
        self, bg_tasks: BackgroundTasks, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> Dish:
        """Получение определенного блюда"""
        cache = await self.cache_repo.get_dish_cache(menu_id, submenu_id, dish_id)
        if cache:
            return cache
        dish = await self.crud_repo.get_specific_dish(menu_id, submenu_id, dish_id)
        discount = await self.cache_repo.get_discount_cache(dish.id)
        update_dish_price(dish, discount)

        bg_tasks.add_task(self.cache_repo.set_dish_cache, menu_id, submenu_id, dish)

        return dish

    async def create_dish(
        self,
        bg_tasks: BackgroundTasks,
        menu_id: UUID,
        submenu_id: UUID,
        data: DishInput,
    ) -> Dish:
        """Добавление нового блюда"""
        dish = await self.crud_repo.create_dish(submenu_id, data)
        bg_tasks.add_task(self.cache_repo.delete_all_dishes_cache, menu_id, submenu_id)
        bg_tasks.add_task(self.cache_repo.delete_menus_tree_cache)

        return dish

    async def update_dish(
        self,
        bg_tasks: BackgroundTasks,
        menu_id: UUID,
        submenu_id: UUID,
        dish_id: UUID,
        data: DishInput,
    ) -> Dish:
        """Изменение блюда"""
        dish = await self.crud_repo.update_dish(menu_id, submenu_id, dish_id, data)
        bg_tasks.add_task(
            self.cache_repo.delete_dish_cache, menu_id, submenu_id, dish_id
        )
        bg_tasks.add_task(self.cache_repo.delete_menus_tree_cache)

        return dish

    async def delete_dish(
        self, bg_tasks: BackgroundTasks, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> None:
        """Удаление блюда"""
        await self.crud_repo.delete_dish(menu_id, submenu_id, dish_id)
        bg_tasks.add_task(self.cache_repo.delete_all_dishes_cache, menu_id, submenu_id)
        bg_tasks.add_task(
            self.cache_repo.delete_dish_cache, menu_id, submenu_id, dish_id
        )
        bg_tasks.add_task(self.cache_repo.delete_menus_tree_cache)
