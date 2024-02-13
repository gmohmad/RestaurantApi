from src.tasks.google_api_config.config import get_sheet_values


class Parser:
    def __init__(self) -> None:
        self.data: list[dict] = []

    async def parser(self) -> list[dict]:
        """Парсинг данных с google таблицы"""
        sheet_values = await get_sheet_values()
        for item in sheet_values:
            if item[0]:
                menu = {
                    'id': item[0],
                    'title': item[1],
                    'description': item[2],
                    'submenus': [],
                }
                self.data.append(menu)
            elif item[1]:
                submenu = {
                    'id': item[1],
                    'title': item[2],
                    'description': item[3],
                    'dishes': [],
                }
                menu['submenus'].append(submenu)
            elif item[2]:
                dish = {
                    'id': item[2],
                    'title': item[3],
                    'description': item[4],
                    'price': float(item[5]),
                    'discount': int(item[6]) if item[6] else 0,
                }
                submenu['dishes'].append(dish)

        return self.data
