from uuid import UUID

from pydantic import BaseModel, field_serializer


class DishInput(BaseModel):
    """Модель для валидации входных данных для создания блюда"""
    id: UUID | None = None
    title: str
    description: str
    price: float


class DishOutput(BaseModel):
    """Модель для валидации выходных данных блюда"""
    id: UUID
    title: str
    description: str
    price: float
    submenu_id: UUID

    @field_serializer('price')
    def serialize_price(self, price: float) -> str:
        """Конвертирует цену в строку"""
        return str(price)


class DishUpdate(BaseModel):
    """Модель для валидации входных данных для изменения блюда"""
    title: str | None = None
    description: str | None = None
    price: float | None = None
