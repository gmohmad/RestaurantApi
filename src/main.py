from fastapi import FastAPI
from src.routers.menu_router import menu_router
from src.routers.submenu_router import submenu_router
from src.routers.dish_router import dish_router


app = FastAPI(title="Y_lab_FastAPI")

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)
