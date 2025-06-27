from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.db.models.films import Films
from app.db import db_session
from app.schemas.film import Film


class MainPageController:
    def __init__(self):
        self.__templates = Jinja2Templates(directory="app/templates")
        self.routers = APIRouter(prefix="/films")
        self.routers.add_api_route('', self.__return_main_page, methods=["GET"])
        self.routers.add_api_route('/get_all', self.__return_main_page, methods=["GET"])


    def __return_main_page(self, request: Request):
            return self.__templates.TemplateResponse("film.html", {"request": request, "list_film": self.__get_films()})

    def __get_films(self) -> list[Film]:
        db_sess = db_session.create_session()
        films = db_sess.query(Films).all()
        res = [Film(id=film.id,
                    name=film.name,
                    description=film.description,
                    id_img=film.img_id,
                    last_modification=film.last_modification) for film in films] * 30
        print(res)
        db_sess.close()
        return res[:-1]
