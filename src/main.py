from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.dish.dish_router import dish_router
from src.api.menu.menu_router import menu_router
from src.api.submenu.submenu_router import submenu_router

app = FastAPI(title='Y_lab_FastAPI')

app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)

app.mount(
    '/openapi',
    StaticFiles(directory='src/api', html=False),
    name='openapi',
)

app.openapi_url = '/openapi/api_specs.yaml'
