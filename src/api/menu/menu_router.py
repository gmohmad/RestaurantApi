from fastapi import APIRouter, Depends, status
from uuid import UUID
from typing import List

from src.schemas.menu_schemas import MenuInput, MenuOutput, MenuUpdate
from src.api.menu.service_repo import MenuServiceRepo
from src.config import MENU_URL, MENUS_URL

menu_router = APIRouter(prefix="/api/v1")


@menu_router.get(MENUS_URL, response_model=List[MenuOutput], name="get_menus")
async def get_all_menus(repo: MenuServiceRepo = Depends()) -> List[MenuOutput]:
    """Получение всех меню"""
    return await repo.get_all_menus()


@menu_router.get(MENU_URL, response_model=MenuOutput, name="get_menu")
async def get_specific_menu(
    target_menu_id: UUID, repo: MenuServiceRepo = Depends()
) -> MenuOutput:
    """Получение определенного меню"""
    return await repo.get_specific_menu(target_menu_id)


@menu_router.patch(MENU_URL, response_model=MenuOutput, name="update_menu")
async def update_menu(
    target_menu_id: UUID, data: MenuUpdate, repo: MenuServiceRepo = Depends()
) -> MenuOutput:
    """Изменение меню"""
    return await repo.update_menu(target_menu_id, data)


@menu_router.post(
    MENUS_URL,
    status_code=status.HTTP_201_CREATED,
    response_model=MenuOutput,
    name="create_menu",
)
async def create_menu(data: MenuInput, repo: MenuServiceRepo = Depends()) -> MenuOutput:
    """Добавление нового меню"""
    return await repo.create_menu(data)


@menu_router.delete(MENU_URL, name="delete_menu")
async def delete_menu(target_menu_id: UUID, repo: MenuServiceRepo = Depends()) -> None:
    """Удаление меню"""
    return await repo.delete_menu(target_menu_id)
