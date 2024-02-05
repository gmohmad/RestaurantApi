from pydantic import BaseModel, field_serializer
from uuid import UUID
from typing import Optional


class DishInput(BaseModel):
    title: str
    description: str
    price: float


class DishOutput(BaseModel):
    id: UUID
    title: str
    description: str
    price: float
    submenu_id: UUID

    @field_serializer("price")
    def serialize_price(self, price: float) -> str:
        return str(price)


class DishUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
