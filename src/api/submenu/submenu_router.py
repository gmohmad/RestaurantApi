from fastapi import APIRouter, Depends, status
from uuid import UUID
from typing import List

from src.api.submenu.service_repo import SubMenuServiceRepo
from src.schemas.submenu_schemas import SubMenuInput, SubMenuOutput, SubMenuUpdate


submenu_router = APIRouter(prefix="/api/v1/menus/{target_menu_id}/submenus")


@submenu_router.get("/", response_model=List[SubMenuOutput])
async def get_all_submenus(
    target_menu_id: UUID, repo: SubMenuServiceRepo = Depends()
) -> List[SubMenuOutput]:
    """Получение всех подменю"""
    return await repo.get_all_submenus(target_menu_id)


@submenu_router.get("/{target_submenu_id}", response_model=SubMenuOutput)
async def get_specific_submenu(
    target_menu_id: UUID, target_submenu_id: UUID, repo: SubMenuServiceRepo = Depends()
) -> SubMenuOutput:
    """Получение определенного подменю"""
    return await repo.get_specific_submenu(target_menu_id, target_submenu_id)


@submenu_router.patch("/{target_submenu_id}", response_model=SubMenuOutput)
async def update_submenu(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    data: SubMenuUpdate,
    repo: SubMenuServiceRepo = Depends(),
) -> SubMenuOutput:
    """Изменение подменю"""
    return await repo.update_submenu(target_menu_id, target_submenu_id, data)


@submenu_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=SubMenuOutput
)
async def create_submenu(
    target_menu_id: UUID, data: SubMenuInput, repo: SubMenuServiceRepo = Depends()
) -> SubMenuOutput:
    """Добавление нового подменю"""
    return await repo.create_submenu(target_menu_id, data)


@submenu_router.delete("/{target_submenu_id}")
async def delete_submenu(
    target_menu_id: UUID, target_submenu_id: UUID, repo: SubMenuServiceRepo = Depends()
) -> None:
    """Удаление подменю"""
    return await repo.delete_submenu(target_menu_id, target_submenu_id)
