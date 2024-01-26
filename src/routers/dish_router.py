from fastapi import APIRouter, Depends, status
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from src.database import get_async_session
from src.models.models import Dish
from src.schemas.dish_schemas import DishInput, DishOutput, DishUpdate
from src.utils import create_dish_helper, get_dish_by_id


dish_router = APIRouter(
    prefix="/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes"
)


@dish_router.get("/", response_model=List[DishOutput])
async def get_all_dishes(
    target_submenu_id: UUID, session: AsyncSession = Depends(get_async_session)
):
    query = select(Dish).where(Dish.submenu_id == target_submenu_id)
    result = await session.execute(query)
    dishes = [dish_tuple[0] for dish_tuple in result.all()]
    return dishes


@dish_router.get("/{target_dish_id}", response_model=DishOutput)
async def get_specific_dish(
    target_menu_id: UUID, 
    target_submenu_id: UUID,
    target_dish_id: UUID, 
    session: AsyncSession = Depends(get_async_session)
):
    dish = await get_dish_by_id(target_menu_id, target_submenu_id, target_dish_id, session)

    return dish


@dish_router.patch("/{target_dish_id}", response_model=DishOutput)
async def update_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    target_dish_id: UUID,
    updated_data: DishUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    dish = await get_dish_by_id(target_menu_id, target_submenu_id, target_dish_id, session)

    for field, value in updated_data.model_dump().items():
        if value is not None:
            setattr(dish, field, value)

    await session.commit()
    await session.refresh(dish)

    return dish


@dish_router.post("/", status_code=status.HTTP_201_CREATED, response_model=DishOutput)
async def create_dish(
    target_submenu_id: UUID,
    new_dish: DishInput,
    session: AsyncSession = Depends(get_async_session),
):
    dish = await create_dish_helper(target_submenu_id, new_dish, session)
    return dish


@dish_router.delete("/{target_dish_id}")
async def delete_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    target_dish_id: UUID, 
    session: AsyncSession = Depends(get_async_session)
):
    dish = await get_dish_by_id(target_menu_id, target_submenu_id, target_dish_id, session)

    await session.delete(dish)
    await session.commit()
