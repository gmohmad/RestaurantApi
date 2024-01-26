from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy import  insert, select, func, and_

from src.database import get_async_session
from src.models.models import Base
from src.schemas.menu_schemas import MenuInput
from src.schemas.submenu_schemas import SubMenuInput
from src.schemas.dish_schemas import DishInput
from src.models.models import Menu, SubMenu, Dish


async def create_menu_helper(data: MenuInput, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Menu).values(**data.model_dump()).returning(Menu)
    result = await session.execute(stmt)
    menu = result.fetchone()[0]

    await session.commit()

    menu.submenus_count, menu.dishes_count = await get_counts_for_menu(menu.id, session)

    return menu


async def create_submenu_helper(
    menu_id: UUID, data: SubMenuInput, session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        insert(SubMenu).values(menu_id=menu_id, **data.model_dump()).returning(SubMenu)
    )
    result = await session.execute(stmt)
    submenu = result.fetchone()[0]

    await session.commit()

    submenu.dishes_count = await get_counts_for_submenu(submenu.id, session)

    return submenu


async def create_dish_helper(
    submenu_id: UUID, data: DishInput, session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        insert(Dish).values(submenu_id=submenu_id, **data.model_dump()).returning(Dish)
    )
    result = await session.execute(stmt)
    dish = result.fetchone()[0]

    await session.commit()

    return dish


async def get_menu_by_id(
    target_menu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    query = await session.execute(select(Menu).where(Menu.id == target_menu_id))
    menu = query.scalar()

    return check_if_exists(menu, "menu")


async def get_submenu_by_id(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
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
):
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


def check_if_exists(obj: Base | None, obj_name: str):
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{obj_name} not found",
        )
    return obj


async def get_counts_for_menu(
    menu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    # Реализация вывода количества подменю и блюд для Меню через один (сложный) ORM запрос
    result = await session.execute(
        select(
            func.count(func.distinct(SubMenu.id)),
            func.count(func.distinct(Dish.id))
        )
        .select_from(Menu)
        .outerjoin(SubMenu)
        .outerjoin(Dish)
        .group_by(Menu.id)
        .where(Menu.id == menu_id)
    )

    submenu_count, dishes_count = result.all()[0]

    return submenu_count, dishes_count


async def get_counts_for_submenu(
    submenu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    dishes_count = await session.scalar(
        select(func.count(Dish.id)).join(SubMenu).where(Dish.submenu_id == submenu_id)
    )
    return dishes_count
