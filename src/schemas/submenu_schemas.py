from uuid import UUID

from pydantic import BaseModel


class SubMenuInput(BaseModel):
    """Модель для валидации входных данных для создания подменю"""
    title: str
    description: str


class SubMenuOutput(BaseModel):
    """Модель для валидации выходных данных подменю"""
    id: UUID
    title: str
    description: str
    dishes_count: int
    menu_id: UUID


class SubMenuUpdate(BaseModel):
    """Модель для валидации входных данных для изменения подменю"""
    title: str | None = None
    description: str | None = None
