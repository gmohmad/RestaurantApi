from uuid import UUID

from fastapi import Depends
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.model_definitions.models import Dish, SubMenu
from src.schemas.dish_schemas import DishInput, DishUpdate
from src.utils import check_if_exists


class DishCRUDRepo:
    """CRUD репозиторий для блюд"""

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self.session = session

    async def get_all_dishes(self, submenu_id: UUID) -> list[Dish]:
        """Получение всех блюд"""
        query = select(Dish).where(Dish.submenu_id == submenu_id)
        result = await self.session.execute(query)
        return result.scalars().fetchall()

    async def create_dish(self, submenu_id: UUID, data: DishInput) -> Dish:
        """Добавление нового блюда"""
        if not data.id:
            del data.id
        dish = Dish(submenu_id=submenu_id, **data.model_dump())

        self.session.add(dish)
        await self.session.commit()
        await self.session.refresh(dish)

        return dish

    async def get_specific_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID
    ) -> Dish:
        """Получение определенного блюда"""
        query = await self.session.execute(
            select(Dish)
            .join(SubMenu)
            .where(
                and_(
                    SubMenu.menu_id == menu_id,
                    SubMenu.id == submenu_id,
                    Dish.submenu_id == submenu_id,
                    Dish.id == dish_id,
                )
            )
        )
        result = query.scalar()

        return check_if_exists(result, 'dish')

    async def update_dish(
        self, menu_id: UUID, submenu_id: UUID, dish_id: UUID, data: DishUpdate
    ) -> Dish:
        """Изменение блюда"""
        dish = await self.get_specific_dish(menu_id, submenu_id, dish_id)

        for field, value in data.model_dump().items():
            if value is not None:
                setattr(dish, field, value)

        await self.session.commit()
        await self.session.refresh(dish)

        return dish

    async def delete_dish(self, menu_id: UUID, submenu_id: UUID, dish_id: UUID) -> None:
        """Удаление блюда"""
        dish = await self.get_specific_dish(menu_id, submenu_id, dish_id)

        await self.session.delete(dish)
        await self.session.commit()
