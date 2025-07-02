from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.db.__all_models import *
from app.db import db_session
from app.schemas.film import Film
from app.schemas.error import Error
from .api_media import ApiMedia
from .api_place import ApiPlace
from .api_img_with_audio import ApiImgWithAudio


class ApiFilms:
    def __init__(self):
        self.routers = APIRouter(prefix="/api")
        self.routers.add_api_route("/get_films", self.get_films, methods=["GET"])
        self.routers.add_api_route("/get_film/{id}", self.get_film, methods=["GET"])
        self.routers.add_api_route("/del_film/{id}", self.del_film, methods=["GET"])
        self.__apiMedia = ApiMedia()
        self.__apiPlace = ApiPlace()
        self.__apiImgWithAudio = ApiImgWithAudio()

    def get_films(self) -> list[Film]:
        db_sess = db_session.create_session()
        films = db_sess.query(Films).all()
        res = [Film(id=film.id,
                    name=film.name,
                    id_img=film.img_id,
                    id_introduction=film.id_introduction,
                    id_conclusion=film.id_conclusion,
                    id_places=[place.id for place in film.places],
                    last_modification=film.last_modification) for film in films]
        db_sess.close()
        return res

    def del_film(self, id: str) -> RedirectResponse:
        db_sess = db_session.create_session()
        film: Films = db_sess.query(Films).filter(Films.id == int(id)).first()
        id_introduction: int = film.id_introduction
        id_conclusion: int = film.id_conclusion
        id_img = film.img_id
        places = [place.id for place in film.places]
        db_sess.delete(film)
        db_sess.commit()
        db_sess.close()
        self.__apiImgWithAudio.del_img_with_audio(id_conclusion)
        self.__apiImgWithAudio.del_img_with_audio(id_introduction)
        self.__apiMedia.del_media(id_img)
        for id in places:
            self.__apiPlace.del_place("0", str(id))
        return RedirectResponse("/", status_code=303)


    def get_film(self, id: str) -> Film | Error:
        db_sess = db_session.create_session()
        try:
            film = db_sess.query(Films).filter(Films.id == int(id)).first()
            response = Film(id=film.id,
                            name=film.name,
                            id_img=film.img_id,
                            id_introduction=film.id_introduction,
                            id_conclusion=film.id_conclusion,
                            id_places=[place.id for place in film.places],
                            last_modification=film.last_modification)
            db_sess.close()
            return response
        except Exception as err:
            print(f"Ошибка в получения фильма по id:\n\t{err}")
            print(err)
            db_sess.close()
            return Error(error="IdError",
                         message="нет такого id",
                         status_code=404)
