from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, status

from src.api.menu.service_repo import MenuServiceRepo
from src.config import MENU_URL, MENUS_TREE, MENUS_URL
from src.schemas.menu_schemas import MenuInput, MenuOutput, MenuUpdate
from src.schemas.menus_tree_schemas import MenusTreeMenuOutput

menu_router = APIRouter(prefix='/api/v1')


@menu_router.get(
    MENUS_TREE, response_model=list[MenusTreeMenuOutput], name='get_menus_tree'
)
async def get_menus_tree(bg_tasks: BackgroundTasks, repo: MenuServiceRepo = Depends()):
    """Получение всех меню с подменю и блюдами связанными с ними"""
    return await repo.get_menus_tree(bg_tasks)


@menu_router.get(MENUS_URL, response_model=list[MenuOutput], name='get_menus')
async def get_all_menus(
    bg_tasks: BackgroundTasks, repo: MenuServiceRepo = Depends()
) -> list[MenuOutput]:
    """Получение всех меню"""
    return await repo.get_all_menus(bg_tasks)


@menu_router.get(MENU_URL, response_model=MenuOutput, name='get_menu')
async def get_specific_menu(
    bg_tasks: BackgroundTasks, target_menu_id: UUID, repo: MenuServiceRepo = Depends()
) -> MenuOutput:
    """Получение определенного меню"""
    return await repo.get_specific_menu(bg_tasks, target_menu_id)


@menu_router.patch(MENU_URL, response_model=MenuOutput, name='update_menu')
async def update_menu(
    bg_tasks: BackgroundTasks,
    target_menu_id: UUID,
    data: MenuUpdate,
    repo: MenuServiceRepo = Depends(),
) -> MenuOutput:
    """Изменение меню"""
    return await repo.update_menu(bg_tasks, target_menu_id, data)


@menu_router.post(
    MENUS_URL,
    status_code=status.HTTP_201_CREATED,
    response_model=MenuOutput,
    name='create_menu',
)
async def create_menu(
    bg_tasks: BackgroundTasks, data: MenuInput, repo: MenuServiceRepo = Depends()
) -> MenuOutput:
    """Добавление нового меню"""
    return await repo.create_menu(bg_tasks, data)


@menu_router.delete(MENU_URL, name='delete_menu')
async def delete_menu(
    bg_tasks: BackgroundTasks, target_menu_id: UUID, repo: MenuServiceRepo = Depends()
) -> None:
    """Удаление меню"""
    return await repo.delete_menu(bg_tasks, target_menu_id)
