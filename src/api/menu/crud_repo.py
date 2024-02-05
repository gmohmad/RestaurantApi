from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.model_definitions.models import Menu
from src.schemas.menu_schemas import MenuInput, MenuUpdate
from src.utils import check_if_exists


class MenuCRUDRepo:
    """CRUD репозиторий для меню"""

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self.session = session

    async def get_all_menus(self) -> list[Menu]:
        """Получение всех меню"""
        query = select(Menu)
        result = await self.session.execute(query)
        return result.scalars().fetchall()

    async def create_menu(self, data: MenuInput) -> Menu:
        """Добавление нового меню"""
        menu = Menu(**data.model_dump())

        self.session.add(menu)
        await self.session.commit()
        await self.session.refresh(menu)

        return menu

    async def get_specific_menu(self, menu_id: UUID) -> Menu:
        """Получение определенного меню"""
        query = await self.session.execute(select(Menu).where(Menu.id == menu_id))
        result = query.scalar()
        return check_if_exists(result, 'menu')

    async def update_menu(self, menu_id: UUID, data: MenuUpdate) -> Menu:
        """Изменение меню"""
        menu = await self.get_specific_menu(menu_id)

        for field, value in data.model_dump().items():
            if value is not None:
                setattr(menu, field, value)

        await self.session.commit()
        await self.session.refresh(menu)

        return menu

    async def delete_menu(self, menu_id: UUID) -> None:
        """Удаление меню"""
        menu = await self.get_specific_menu(menu_id)

        await self.session.delete(menu)
        await self.session.commit()
