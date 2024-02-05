from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.api.dish.service_repo import DishServiceRepo
from src.config import DISH_URL, DISHES_URL
from src.schemas.dish_schemas import DishInput, DishOutput, DishUpdate

dish_router = APIRouter(prefix='/api/v1')


@dish_router.get(DISHES_URL, response_model=list[DishOutput], name='get_dishes')
async def get_all_dishes(
    target_menu_id: UUID, target_submenu_id: UUID, repo: DishServiceRepo = Depends()
) -> list[DishOutput]:
    """Получение всех блюд"""
    return await repo.get_all_dishes(target_menu_id, target_submenu_id)


@dish_router.get(DISH_URL, response_model=DishOutput, name='get_dish')
async def get_specific_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    target_dish_id: UUID,
    repo: DishServiceRepo = Depends(),
) -> DishOutput:
    """Получение определенного блюда"""
    return await repo.get_specific_dish(
        target_menu_id, target_submenu_id, target_dish_id
    )


@dish_router.patch(DISH_URL, response_model=DishOutput, name='update_dish')
async def update_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    target_dish_id: UUID,
    data: DishUpdate,
    repo: DishServiceRepo = Depends(),
) -> DishOutput:
    """Изменение блюда"""
    return await repo.update_dish(
        target_menu_id, target_submenu_id, target_dish_id, data
    )


@dish_router.post(
    DISHES_URL,
    status_code=status.HTTP_201_CREATED,
    response_model=DishOutput,
    name='create_dish',
)
async def create_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    data: DishInput,
    repo: DishServiceRepo = Depends(),
) -> DishOutput:
    """Добавление нового блюда"""
    return await repo.create_dish(target_menu_id, target_submenu_id, data)


@dish_router.delete(DISH_URL, name='delete_dish')
async def delete_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    target_dish_id: UUID,
    repo: DishServiceRepo = Depends(),
) -> None:
    """Удаление блюда"""
    return await repo.delete_dish(target_menu_id, target_submenu_id, target_dish_id)
