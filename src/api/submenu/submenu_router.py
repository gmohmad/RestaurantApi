from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, status

from src.api.submenu.service_repo import SubMenuServiceRepo
from src.config import SUBMENU_URL, SUBMENUS_URL
from src.schemas.submenu_schemas import SubMenuInput, SubMenuOutput, SubMenuUpdate

submenu_router = APIRouter(prefix='/api/v1')


@submenu_router.get(
    SUBMENUS_URL, response_model=list[SubMenuOutput], name='get_submenus'
)
async def get_all_submenus(
    bg_tasks: BackgroundTasks,
    target_menu_id: UUID,
    repo: SubMenuServiceRepo = Depends(),
) -> list[SubMenuOutput]:
    """Получение всех подменю"""
    return await repo.get_all_submenus(bg_tasks, target_menu_id)


@submenu_router.get(SUBMENU_URL, response_model=SubMenuOutput, name='get_submenu')
async def get_specific_submenu(
    bg_tasks: BackgroundTasks,
    target_menu_id: UUID,
    target_submenu_id: UUID,
    repo: SubMenuServiceRepo = Depends(),
) -> SubMenuOutput:
    """Получение определенного подменю"""
    return await repo.get_specific_submenu(bg_tasks, target_menu_id, target_submenu_id)


@submenu_router.patch(SUBMENU_URL, response_model=SubMenuOutput, name='update_submenu')
async def update_submenu(
    bg_tasks: BackgroundTasks,
    target_menu_id: UUID,
    target_submenu_id: UUID,
    data: SubMenuUpdate,
    repo: SubMenuServiceRepo = Depends(),
) -> SubMenuOutput:
    """Изменение подменю"""
    return await repo.update_submenu(bg_tasks, target_menu_id, target_submenu_id, data)


@submenu_router.post(
    SUBMENUS_URL,
    status_code=status.HTTP_201_CREATED,
    response_model=SubMenuOutput,
    name='create_submenu',
)
async def create_submenu(
    bg_tasks: BackgroundTasks,
    target_menu_id: UUID,
    data: SubMenuInput,
    repo: SubMenuServiceRepo = Depends(),
) -> SubMenuOutput:
    """Добавление нового подменю"""
    return await repo.create_submenu(bg_tasks, target_menu_id, data)


@submenu_router.delete(SUBMENU_URL, name='delete_submenu')
async def delete_submenu(
    bg_tasks: BackgroundTasks,
    target_menu_id: UUID,
    target_submenu_id: UUID,
    repo: SubMenuServiceRepo = Depends(),
) -> None:
    """Удаление подменю"""
    return await repo.delete_submenu(bg_tasks, target_menu_id, target_submenu_id)
