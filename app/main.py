from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.db import db_session
from app.endpoints.api_image import ApiImage
from app.endpoints.form_add_film import FormAddFilm
from app.endpoints.mainPageController import MainPageController

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

db_session.global_init("app/db/database/database.db")
templates = Jinja2Templates(directory="app/templates")

apiImg = ApiImage()
formAddFilm = FormAddFilm()
mainPageController = MainPageController()

app.include_router(apiImg.routres)
app.include_router(formAddFilm.router)
app.include_router(mainPageController.routers)


@app.get("/")
def main_page():
    return RedirectResponse("/films")