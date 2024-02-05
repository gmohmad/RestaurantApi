from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class MenuInput(BaseModel):
    title: str
    description: str


class MenuOutput(BaseModel):
    id: UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class MenuUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
