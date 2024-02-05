from uuid import UUID

from pydantic import BaseModel


class SubMenuInput(BaseModel):
    title: str
    description: str


class SubMenuOutput(BaseModel):
    id: UUID
    title: str
    description: str
    dishes_count: int
    menu_id: UUID


class SubMenuUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
