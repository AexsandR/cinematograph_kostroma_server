from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.db import db_session
from app.endpoints.api_media import ApiMedia
from app.endpoints.form_add import FormAdd
from app.endpoints.pageController import PageController
from app.endpoints.edit_form import FormEdit
from app.endpoints.api_films import ApiFilms
from app.endpoints.api_place import ApiPlace
from app.endpoints.api_img_with_audio import ApiImgWithAudio
from app.endpoints.api_questions import ApiQuestions

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

db_session.global_init("app/db/database/database.db")
templates = Jinja2Templates(directory="app/templates")

apiMedia = ApiMedia()
apiFilm = ApiFilms()
formAdd = FormAdd()
formEdit = FormEdit()
apiPlace = ApiPlace()
mainPageController = PageController()
apiImgWithAudio = ApiImgWithAudio()
apiQuestions = ApiQuestions()

app.include_router(apiMedia.routres)
app.include_router(formAdd.router)
app.include_router(mainPageController.routers)
app.include_router(formEdit.router)
app.include_router(apiFilm.routers)
app.include_router(apiPlace.routers)
app.include_router(apiImgWithAudio.router)
app.include_router(apiQuestions.router)


@app.get("/")
def main_page():
    return RedirectResponse("/films")
