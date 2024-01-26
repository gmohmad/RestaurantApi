from fastapi import APIRouter, Depends, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from src.database import get_async_session
from src.models.models import Menu
from src.schemas.menu_schemas import MenuInput, MenuOutput, MenuUpdate
from src.utils import create_menu_helper, get_menu_by_id, get_counts_for_menu


menu_router = APIRouter(prefix="/api/v1/menus")


@menu_router.get("/", response_model=List[MenuOutput])
async def get_all_menus(session: AsyncSession = Depends(get_async_session)):
    query = select(Menu)
    result = await session.execute(query)
    menus_with_counts = []

    for menu_tuple in result.all():
        menu = menu_tuple[0]

        menu.submenus_count, menu.dishes_count = await get_counts_for_menu(
            menu.id, session
        )

        menus_with_counts.append(menu)

    return menus_with_counts


@menu_router.get("/{target_menu_id}", response_model=MenuOutput)
async def get_specific_menu(
    target_menu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    menu = await get_menu_by_id(target_menu_id, session)

    menu.submenus_count, menu.dishes_count = await get_counts_for_menu(menu.id, session)

    return menu


@menu_router.patch("/{target_menu_id}", response_model=MenuOutput)
async def update_menu(
    target_menu_id: UUID,
    updated_data: MenuUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    menu = await get_menu_by_id(target_menu_id, session)

    for field, value in updated_data.model_dump().items():
        if value is not None:
            setattr(menu, field, value)

    await session.commit()
    await session.refresh(menu)

    menu.submenus_count, menu.dishes_count = await get_counts_for_menu(menu.id, session)

    return menu


@menu_router.post("/", status_code=status.HTTP_201_CREATED, response_model=MenuOutput)
async def create_menu(
    new_menu: MenuInput, session: AsyncSession = Depends(get_async_session)
):
    menu = await create_menu_helper(new_menu, session) 
    return menu


@menu_router.delete("/{target_menu_id}")
async def delete_menu(
    target_menu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    menu = await get_menu_by_id(target_menu_id, session)

    await session.delete(menu)
    await session.commit()
