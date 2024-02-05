from uuid import UUID

from pydantic import BaseModel


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
    title: str | None = None
    description: str | None = None
