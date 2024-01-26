from fastapi import APIRouter, Depends, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from src.database import get_async_session
from src.models.models import SubMenu
from src.schemas.submenu_schemas import SubMenuInput, SubMenuOutput, SubMenuUpdate
from src.utils import create_submenu_helper, get_submenu_by_id, get_counts_for_submenu


submenu_router = APIRouter(prefix="/api/v1/menus/{target_menu_id}/submenus")


@submenu_router.get("/", response_model=List[SubMenuOutput])
async def get_all_submenus(
    target_menu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    query = select(SubMenu).where(SubMenu.menu_id == target_menu_id)
    result = await session.execute(query)
    submenus_with_counts = []

    for submenu_tuple in result.all():
        submenu = submenu_tuple[0]

        submenu.dishes_count = await get_counts_for_submenu(submenu.id, session)

        submenus_with_counts.append(submenu)

    return submenus_with_counts


@submenu_router.get("/{target_submenu_id}", response_model=SubMenuOutput)
async def get_specific_submenu(
    target_menu_id: UUID,
    target_submenu_id: UUID, 
    session: AsyncSession = Depends(get_async_session)
):
    submenu = await get_submenu_by_id(target_menu_id, target_submenu_id, session)

    submenu.dishes_count = await get_counts_for_submenu(submenu.id, session)
    return submenu


@submenu_router.patch("/{target_submenu_id}", response_model=SubMenuOutput)
async def update_submenu(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    updated_data: SubMenuUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    submenu = await get_submenu_by_id(target_menu_id, target_submenu_id, session)

    for field, value in updated_data.model_dump().items():
        if value is not None:
            setattr(submenu, field, value)

    await session.commit()
    await session.refresh(submenu)

    submenu.dishes_count = await get_counts_for_submenu(submenu.id, session)

    return submenu


@submenu_router.post("/", status_code=status.HTTP_201_CREATED, response_model=SubMenuOutput)
async def create_submenu(
    target_menu_id: UUID,
    new_submenu: SubMenuInput,
    session: AsyncSession = Depends(get_async_session),
):
    submenu = await create_submenu_helper(target_menu_id, new_submenu, session)
    return submenu


@submenu_router.delete("/{target_submenu_id}")
async def delete_submenu(
    target_menu_id: UUID,
    target_submenu_id: UUID, 
    session: AsyncSession = Depends(get_async_session)
):
    submenu = await get_submenu_by_id(target_menu_id, target_submenu_id, session)

    await session.delete(submenu)
    await session.commit()
