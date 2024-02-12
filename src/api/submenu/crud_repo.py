from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.model_definitions.models import SubMenu
from src.schemas.submenu_schemas import SubMenuInput, SubMenuUpdate
from src.utils import check_if_exists


class SubMenuCRUDRepo:
    """CRUD репозиторий для подменю"""

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self.session = session

    async def get_all_submenus(self, menu_id: UUID) -> list[SubMenu]:
        """Получение всех подменю"""
        query = select(SubMenu).where(SubMenu.menu_id == menu_id)
        result = await self.session.execute(query)
        return result.scalars().fetchall()

    async def create_submenu(self, menu_id: UUID, data: SubMenuInput) -> SubMenu:
        """Добавление нового подменю"""
        if not data.id:
            del data.id
        submenu = SubMenu(menu_id=menu_id, **data.model_dump())

        self.session.add(submenu)
        await self.session.commit()
        await self.session.refresh(submenu)

        return submenu

    async def get_specific_submenu(self, menu_id: UUID, submenu_id: UUID) -> SubMenu:
        """Получение определенного подменю"""
        query = await self.session.execute(
            select(SubMenu).where(SubMenu.menu_id == menu_id, SubMenu.id == submenu_id)
        )
        result = query.scalar()

        return check_if_exists(result, 'submenu')

    async def update_submenu(
        self, menu_id: UUID, submenu_id: UUID, data: SubMenuUpdate
    ) -> SubMenu:
        """Изменение подменю"""
        submenu = await self.get_specific_submenu(menu_id, submenu_id)

        for field, value in data.model_dump().items():
            if value is not None:
                setattr(submenu, field, value)

        await self.session.commit()
        await self.session.refresh(submenu)

        return submenu

    async def delete_submenu(self, menu_id: UUID, submenu_id: UUID) -> None:
        """Удаление подменю"""
        submenu = await self.get_specific_submenu(menu_id, submenu_id)

        await self.session.delete(submenu)
        await self.session.commit()
