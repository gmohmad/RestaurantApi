import uuid
from typing import Any

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Text,
    func,
    select,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property, declarative_base, relationship

metadata = MetaData()
Base: Any = declarative_base(metadata=metadata)


class Dish(Base):
    """Модель блюда"""

    __tablename__ = 'dishes'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    price = Column(Numeric(precision=8, scale=2), nullable=False)
    discount = Column(Integer, default=0)

    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))
    submenu = relationship('SubMenu', back_populates='dishes')


class SubMenu(Base):
    """Модель подменю"""

    __tablename__ = 'submenus'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)

    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship(
        'Dish', back_populates='submenu', cascade='all, delete-orphan'
    )
    dishes_count = column_property(
        select(func.count(Dish.id))
        .where(Dish.submenu_id == id)
        .correlate_except(Dish)
        .scalar_subquery()
    )


class Menu(Base):
    """Модель меню"""

    __tablename__ = 'menus'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
    )
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)

    submenus = relationship(
        'SubMenu', back_populates='menu', cascade='all, delete-orphan'
    )
    submenus_count = column_property(
        select(func.count(SubMenu.id))
        .where(SubMenu.menu_id == id)
        .correlate_except(SubMenu)
        .scalar_subquery()
    )

    dishes_count = column_property(
        select(func.count(Dish.id))
        .join(SubMenu, Dish.submenu_id == SubMenu.id)
        .where(SubMenu.menu_id == id)
        .correlate_except(Dish, SubMenu)
        .scalar_subquery()
    )
