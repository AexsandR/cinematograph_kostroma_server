from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.db import db_session
from app.endpoints.api_image import ApiImages
from app.endpoints.form_add import FormAdd
from app.endpoints.pageController import PageController
from app.endpoints.edit_form import FormEdit
from app.endpoints.api_films import ApiFilms

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

db_session.global_init("app/db/database/database.db")
templates = Jinja2Templates(directory="app/templates")

apiImgs = ApiImages()
apiFilm = ApiFilms()
formAdd = FormAdd()
formEdit = FormEdit()
mainPageController = PageController()

app.include_router(apiImgs.routres)
app.include_router(formAdd.router)
app.include_router(mainPageController.routers)
app.include_router(formEdit.router)
app.include_router(apiFilm.routers)


@app.get("/")
def main_page():
    return RedirectResponse("/films")
