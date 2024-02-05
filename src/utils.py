from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import select, and_

from src.database import get_async_session
from src.models.models import Base

from src.models.models import Menu, SubMenu, Dish


async def get_menu_by_id(
    target_menu_id: UUID, session: AsyncSession = Depends(get_async_session)
) -> Menu:
    query = await session.execute(select(Menu).where(Menu.id == target_menu_id))
    menu = query.scalar()

    return check_if_exists(menu, "menu")


async def get_submenu_by_id(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
) -> SubMenu:
    query = await session.execute(
        select(SubMenu).where(
            and_(SubMenu.menu_id == target_menu_id, SubMenu.id == target_submenu_id)
        )
    )
    submenu = query.scalar()

    return check_if_exists(submenu, "submenu")


async def get_dish_by_id(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    target_dish_id: UUID,
    session: AsyncSession = Depends(get_async_session),
) -> Dish:
    query = await session.execute(
        select(Dish)
        .join(SubMenu)
        .where(
            and_(
                SubMenu.menu_id == target_menu_id,
                SubMenu.id == target_submenu_id,
                Dish.submenu_id == target_submenu_id,
                Dish.id == target_dish_id,
            )
        )
    )
    dish = query.scalar()

    return check_if_exists(dish, "dish")


def check_if_exists(obj: Base | None, obj_name: str) -> Base:
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{obj_name} not found",
        )
    return obj
