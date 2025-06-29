from xml.sax import parse

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.db.__all_models import *
from app.db import db_session
from app.schemas.film import Film
from app.schemas.error import Error
from app.schemas.place import Place


class ApiPlace:
    def __init__(self):
        self.routers = APIRouter(prefix="/api")
        self.routers.add_api_route("/get_place", self.get_films, methods=["GET"])

    # def get_place(self) -> list[Place]:
    #     db_sess = db_session.create_session()
    #     places = db_sess.query(Places).all()
    #     res = [Place(id=place.id,
    #                  name=place.name_place,
    #                  description=place.description,
    #                  latitude=place.latitude,
    #                  longitude=place.longitude,
    #                  rado
    #                  ) for place in places]
    #     db_sess.close()
    #     return res

    def del_film(self, id: str) -> RedirectResponse:
        db_sess = db_session.create_session()
        try:
            film: Films = db_sess.query(Films).filter(Films.id == str(id)).first()
            preview: Images = db_sess.query(Images).filter(Images.id == film.img_id).first()
            frame: Images = db_sess.query(Images).filter(Images.id == film.frame_id).first()
            db_sess.delete(film)
            db_sess.delete(preview)
            db_sess.delete(frame)
            db_sess.commit()
            db_sess.close()
            return RedirectResponse("/", status_code=303)
        except Exception as err:
            print(f"Ошибка в удалении фильма:\n\t{err}")
            db_sess.close()
            return RedirectResponse("/", status_code=404)

    def get_film(self, id: str) -> Film | Error:
        db_sess = db_session.create_session()
        try:
            film = db_sess.query(Films).filter(Films.id == int(id)).first()
            db_sess.close()
            return Film(id=film.id, name=film.name, description=film.description, id_img=film.img_id,
                        id_frame=film.frame_id,
                        last_modification=film.last_modification)
        except Exception as err:
            print(f"Ошибка в получения фильма по id:\n\t{err}")
            print(err)
            db_sess.close()
            return Error(error="IdError",
                         message="нет такого id",
                         status_code=404)
