from http.client import responses
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
        self.routers.add_api_route("/get_place/{id_film}", self.get_places, methods=["GET"])

    def get_places(self, id_film: str) -> list[Place]:
        db_sess = db_session.create_session()
        film: Films = db_sess.query(Films).filter(Films.id == id_film).first()
        places = film.places
        response: list[Place] = []
        for place in places:
            response.append(
                Place(
                    id=place.id,
                    name_place=place.name_place,
                    id_question=place.id_question,
                    latitude=place.latitude,
                    longitude=place.longitude,
                    radius=place.radius,
                    img_id=place.img_id,
                    fact_id=place.fact_id,
                    hints_id=[img.id for img in place.hints],
                    last_modification=place.last_modification
                )
            )

        db_sess.close()
        return response


def del_place(self, id_place: str) -> RedirectResponse:
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
