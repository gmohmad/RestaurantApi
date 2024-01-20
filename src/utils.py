from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select, func


from src.database import get_async_session
from src.models.models import Base
from src.models.models import Menu, SubMenu, Dish


async def get_object_by_id(
    target_object_id: UUID,
    object: Base,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(object).where(object.id == target_object_id))
    entity = result.scalar()

    if entity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{object.__name__.lower()} not found",
        )
    return entity


async def get_counts_for_menu(
    menu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    submenus_count = await session.scalar(
        select(func.count(SubMenu.id)).join(Menu).where(SubMenu.menu_id == menu_id)
    )
    dishes_count = await session.scalar(
        select(func.count(Dish.id))
        .join(SubMenu)
        .join(Menu)
        .where(SubMenu.menu_id == menu_id)
    )

    return submenus_count, dishes_count


async def get_counts_for_submenu(
    submenu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    dishes_count = await session.scalar(
        select(func.count(Dish.id)).join(SubMenu).where(Dish.submenu_id == submenu_id)
    )
    return dishes_count


def convert_price(dish: dict):
    dish.price = str(dish.price)
    return dish
