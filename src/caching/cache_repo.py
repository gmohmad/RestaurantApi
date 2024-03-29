import pickle
from uuid import UUID

from aioredis import Redis
from fastapi import Depends

from src.database import get_redis
from src.model_definitions.models import Dish, Menu, SubMenu

MENU_KEY = 'menus/{}'
SUBMENU_KEY = 'menus/{}/submenus/'
DISH_KEY = 'menus/{}/submenus/{}/dishes/'


class CacheRepo:
    """Cache репозиторий для объктов меню, подменю и блюда"""

    def __init__(self, redis: Redis = Depends(get_redis)) -> None:
        self.redis = redis

    async def get_discount_cache(self, dish_id: UUID) -> int | None:
        discount = await self.redis.get(str(dish_id))
        if discount is not None:
            return pickle.loads(discount)
        return None

    async def delete_cache_by_mask(self, pattern: str) -> None:
        """Удаление кэша по маске"""
        for key in await self.redis.keys(pattern + '*'):
            await self.redis.delete(key)

    async def get_menus_tree_cache(self) -> list[Menu] | None:
        """Получение кэша эндпойнта get_menus_tree"""
        cached_menus_tree = await self.redis.get('menus_tree')
        if cached_menus_tree:
            return pickle.loads(cached_menus_tree)
        return None

    async def set_menus_tree_cache(self, menus_tree: list[Menu]) -> None:
        """Добавление кэша для эндпойнта get_menus_tree"""
        await self.redis.set('menus_tree', pickle.dumps(menus_tree), 3600)

    async def delete_menus_tree_cache(self) -> None:
        """Удаление кэша эндпойнта get_menus_tree"""
        await self.redis.delete('menus_tree')

    async def get_all_menus_cache(self) -> list[Menu] | None:
        """Получение кэша эндпойнта get_all_menus"""
        cached_menus = await self.redis.get(MENU_KEY)
        if cached_menus:
            return pickle.loads(cached_menus)
        return None

    async def set_all_menus_cache(self, menus: list[Menu]) -> None:
        """Добавление кэша для эндпойнта get_all_menus"""
        await self.redis.set(MENU_KEY, pickle.dumps(menus), 3600)

    async def get_menu_cache(self, menu_id: UUID) -> Menu | None:
        """Получение кэша эндпойнта get_specific_menu"""
        cached_menu = await self.redis.get(MENU_KEY.format(menu_id))
        if cached_menu:
            return pickle.loads(cached_menu)
        return None

    async def set_menu_cache(self, menu: Menu) -> None:
        """Добавление кэша для эндпойнта get_specific_menu"""
        await self.redis.set(MENU_KEY.format(menu.id), pickle.dumps(menu), 3600)

    async def delete_all_menu_cache(self) -> None:
        """Удаление кэша эндпойнта get_all_menus"""
        await self.redis.delete(MENU_KEY)

    async def delete_menu_cache(self, menu_id: UUID) -> None:
        """Удаление кэша эндпойнтов get_all_menus и get_specific_menu"""
        await self.redis.delete(MENU_KEY.format(menu_id))
        await self.delete_all_menu_cache()

    async def delete_menu_tree_cache(self, menu_id: UUID) -> None:
        """Удаление кэша для всех эндпойнтов связанных с определенным меню"""
        await self.delete_cache_by_mask(MENU_KEY.format(menu_id))

    async def get_all_submenus_cache(self, menu_id: UUID) -> list[SubMenu] | None:
        """Получение кэша эндпойнта get_all_submenus"""
        cached_submenus = await self.redis.get(SUBMENU_KEY.format(menu_id))
        if cached_submenus:
            return pickle.loads(cached_submenus)
        return None

    async def set_all_submenus_cache(
        self, menu_id: UUID, submenus: list[SubMenu]
    ) -> None:
        """Добавление кэша для эндпойнта get_all_submenus"""
        await self.redis.set(SUBMENU_KEY.format(menu_id), pickle.dumps(submenus), 3600)

    async def get_submenu_cache(
        self, menu_id: UUID, submenu_id: UUID
    ) -> SubMenu | None:
        """Получение кэша эндпойнта get_specific_submenu"""
        cached_submenu = await self.redis.get(
            SUBMENU_KEY.format(menu_id) + str(submenu_id)
        )
        if cached_submenu:
            return pickle.loads(cached_submenu)
        return None

    async def set_submenu_cache(self, menu_id: UUID, submenu: SubMenu) -> None:
        """Добавление кэша для эндпойнта get_specific_submenu"""
        await self.redis.set(
            SUBMENU_KEY.format(menu_id) + str(submenu.id), pickle.dumps(submenu), 3600
        )

    async def delete_all_submenu_cache(self, menu_id: UUID) -> None:
        """Удаление кэша эндпойнта get_all_submenus и связанных меню"""
        await self.redis.delete(SUBMENU_KEY.format(menu_id))
        await self.delete_menu_cache(menu_id)

    async def delete_submenu_cache(self, menu_id: UUID, submenu_id: UUID) -> None:
        """Удаление кэша эндпойнтов get_all_submenus и get_specific_submenu и связанных меню"""
        await self.redis.delete(SUBMENU_KEY.format(menu_id) + str(submenu_id))
        await self.redis.delete(SUBMENU_KEY.format(menu_id))

    async def delete_submenu_tree_cache(self, menu_id: UUID, submenu_id: UUID) -> None:
        """Удаление кэша для всех эндпойнтов связанных с определенным подменю"""
        await self.delete_cache_by_mask(SUBMENU_KEY.format(menu_id) + str(submenu_id))

    async def get_all_dishes_cache(
        self, menu_id: UUID, submenu_id: UUID
    ) -> list[Dish] | None:
        """Получение кэша эндпойнта get_all_dishes"""
        cached_dishes = await self.redis.get(DISH_KEY.format(menu_id, submenu_id))
        if cached_dishes:
            return pickle.loads(cached_dishes)
        return None

    async def set_all_dishes_cache(
        self, menu_id: UUID, submenu_id: UUID, dishes: list[Dish]
    ) -> None:
        """Добавление кэша для эндпойнта get_all_dishes"""
        await self.redis.set(
            DISH_KEY.format(menu_id, submenu_id), pickle.dumps(dishes), 3600
        )

    async def get_dish_cache(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> Dish | None:
        """Получение кэша эндпойнта get_specific_dish"""
        cached_dish = await self.redis.get(
            DISH_KEY.format(menu_id, submenu_id) + str(dish_id)
        )
        if cached_dish:
            return pickle.loads(cached_dish)
        return None

    async def set_dish_cache(self, menu_id: UUID, submenu_id: UUID, dish: Dish) -> None:
        """Добавление кэша для эндпойнта get_specific_dish"""
        await self.redis.set(
            DISH_KEY.format(menu_id, submenu_id) + str(dish.id),
            pickle.dumps(dish),
            3600,
        )

    async def delete_all_dishes_cache(self, menu_id: UUID, submenu_id: UUID) -> None:
        """Удаление кэша для всех эндпойнтов связанных с определенным блюда"""
        await self.redis.delete(DISH_KEY.format(menu_id, submenu_id))
        await self.delete_all_submenu_cache(menu_id)
        await self.delete_submenu_cache(menu_id, submenu_id)

    async def delete_dish_cache(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> None:
        """Удаление кэша для всех эндпойнтов связанных с определенным блюда"""
        await self.redis.delete(DISH_KEY.format(menu_id, submenu_id) + str(dish_id))
        await self.redis.delete(DISH_KEY.format(menu_id, submenu_id))
