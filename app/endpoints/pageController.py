from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.endpoints.api_films import ApiFilms
from app.endpoints.api_place import ApiPlace


class PageController:
    def __init__(self):
        self.__templates = Jinja2Templates(directory="app/templates")
        self.routers = APIRouter(prefix="/films")
        self.routers.add_api_route('', self.__return_film_page, methods=["GET"])
        self.routers.add_api_route('/place/{id_film}', self.__return_place_page, methods=["GET"])
        self.__apiFilm = ApiFilms()
        self.__apiPlace = ApiPlace()

    def __return_film_page(self, request: Request):
        return self.__templates.TemplateResponse("film.html",
                                                 {"request": request, "list_film": self.__apiFilm.get_films()})

    def __return_place_page(self, request: Request, id_film: str):
        return self.__templates.TemplateResponse("place.html",
                                                 {"request": request, "id": id_film,
                                                  "list_places": self.__apiPlace.get_places(int(id_film))})
