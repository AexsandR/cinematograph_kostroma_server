from http.client import HTTPResponse

from fastapi import APIRouter, UploadFile, Request, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db import db_session
from app.db.__all_models import Images, Films, FramesNovela
from app.endpoints.api_films import ApiFilms


class FormEdit:
    def __init__(self, ):
        self.__templates = Jinja2Templates(directory="app/templates")
        self.router = APIRouter(prefix="/editForm")
        # self.router.add_api_route("/film", self, methods=["POST"], response_model=None)
        self.router.add_api_route("/film/{id}", self.__show_form_film, methods=["GET"], response_model=None)
        self.__apiFilm = ApiFilms()

    def __show_form_film(self, request: Request, id: str) -> HTMLResponse | RedirectResponse:
        try:
            print("000000")
            film = self.__apiFilm.get_film(id)
            print("000000 ", film.name, film.description)
            return self.__templates.TemplateResponse("edit_form_film.html",
                                                     {"request": request, "error": False, "type": "film",
                                                      "name": film.name, "description": film.description,
                                                      "id_img": film.id_img})
        except Exception as err:
            print(err)
            return  RedirectResponse("/")


    def __show_form_place(self, request: Request) -> HTMLResponse:
        return self.__templates.TemplateResponse("form_add_film.html",
                                                 {"request": request, "error": False, "type": "place"})
