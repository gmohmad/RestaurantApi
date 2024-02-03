from fastapi import APIRouter, Depends, status
from uuid import UUID
from typing import List

from src.api.dish.service_repo import DishServiceRepo
from src.schemas.dish_schemas import DishInput, DishOutput, DishUpdate


dish_router = APIRouter(
    prefix="/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes"
)


@dish_router.get("/", response_model=List[DishOutput])
async def get_all_dishes(
    target_menu_id: UUID, target_submenu_id: UUID, repo: DishServiceRepo = Depends()
):
    """Получение всех блюд"""
    return await repo.get_all_dishes(target_menu_id, target_submenu_id)


@dish_router.get("/{target_dish_id}", response_model=DishOutput)
async def get_specific_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    target_dish_id: UUID,
    repo: DishServiceRepo = Depends(),
):
    """Получение определенного блюда"""
    return await repo.get_specific_dish(
        target_menu_id, target_submenu_id, target_dish_id
    )


@dish_router.patch("/{target_dish_id}", response_model=DishOutput)
async def update_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    target_dish_id: UUID,
    data: DishUpdate,
    repo: DishServiceRepo = Depends(),
):
    """Изменение блюда"""
    return await repo.update_dish(
        target_menu_id, target_submenu_id, target_dish_id, data
    )


@dish_router.post("/", status_code=status.HTTP_201_CREATED, response_model=DishOutput)
async def create_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    data: DishInput,
    repo: DishServiceRepo = Depends(),
):
    """Добавление нового блюда"""
    return await repo.create_dish(target_menu_id, target_submenu_id, data)


@dish_router.delete("/{target_dish_id}")
async def delete_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    target_dish_id: UUID,
    repo: DishServiceRepo = Depends(),
):
    """Удаление блюда"""
    return await repo.delete_dish(target_menu_id, target_submenu_id, target_dish_id)
