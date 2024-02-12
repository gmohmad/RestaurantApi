from uuid import UUID

from pydantic import BaseModel


class MenuInput(BaseModel):
    """Модель для валидации входных данных для создания меню"""
    id: UUID | None = None
    title: str
    description: str


class MenuOutput(BaseModel):
    """Модель для валидации выходных данных меню"""
    id: UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class MenuUpdate(BaseModel):
    """Модель для валидации входных данных для изменения меню"""
    title: str | None = None
    description: str | None = None
