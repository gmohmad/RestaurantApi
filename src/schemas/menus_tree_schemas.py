from src.schemas.dish_schemas import DishOutput
from src.schemas.menu_schemas import MenuOutput
from src.schemas.submenu_schemas import SubMenuOutput


class MenuTreeSubmenuOutput(SubMenuOutput):
    dishes: list[DishOutput]


class MenusTreeMenuOutput(MenuOutput):
    submenus: list[MenuTreeSubmenuOutput]
