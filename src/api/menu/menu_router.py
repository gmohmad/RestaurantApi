from fastapi import APIRouter, Depends, status
from uuid import UUID
from typing import List

from src.schemas.menu_schemas import MenuInput, MenuOutput, MenuUpdate
from src.api.menu.service_repo import MenuServiceRepo


menu_router = APIRouter(prefix="/api/v1/menus")


@menu_router.get("/", response_model=List[MenuOutput])
async def get_all_menus(repo: MenuServiceRepo = Depends()) -> List[MenuOutput]:
    """Получение всех меню"""
    return await repo.get_all_menus()


@menu_router.get("/{target_menu_id}", response_model=MenuOutput)
async def get_specific_menu(
    target_menu_id: UUID, repo: MenuServiceRepo = Depends()
) -> MenuOutput:
    """Получение определенного меню"""
    return await repo.get_specific_menu(target_menu_id)


@menu_router.patch("/{target_menu_id}", response_model=MenuOutput)
async def update_menu(
    target_menu_id: UUID, data: MenuUpdate, repo: MenuServiceRepo = Depends()
) -> MenuOutput:
    """Изменение меню"""
    return await repo.update_menu(target_menu_id, data)


@menu_router.post("/", status_code=status.HTTP_201_CREATED, response_model=MenuOutput)
async def create_menu(data: MenuInput, repo: MenuServiceRepo = Depends()) -> MenuOutput:
    """Добавление нового меню"""
    return await repo.create_menu(data)


@menu_router.delete("/{target_menu_id}")
async def delete_menu(target_menu_id: UUID, repo: MenuServiceRepo = Depends()) -> None:
    """Удаление меню"""
    return await repo.delete_menu(target_menu_id)
