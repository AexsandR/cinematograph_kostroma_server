from fastapi import APIRouter
from app.db.models.films import Films
from app.db import db_session
from app.schemas.film import Film
from app.schemas.error import Error


class ApiFilms:
    def __init__(self):
        self.routers = APIRouter(prefix="/api")
        self.routers.add_api_route("/get_films", self.get_films, methods=["GET"])
        self.routers.add_api_route("/get_film/{id}", self.get_film, methods=["GET"])

    def get_films(self) -> list[Film]:
            db_sess = db_session.create_session()
            films = db_sess.query(Films).all()
            res = [Film(id=film.id,
                        name=film.name,
                        description=film.description,
                        id_img=film.img_id,
                        last_modification=film.last_modification) for film in films] * 30
            db_sess.close()
            return res[:-1]

    def get_film(self, id: str) -> Film | Error:
        db_sess = db_session.create_session()
        try:
            film = db_sess.query(Films).filter(Films.id == int(id)).first()

            return Film(id=film.id, name=film.name, description=film.description, id_img=film.img_id,
                        last_modification=film.last_modification)
        except Exception as err:
            print(err)
            db_sess.close()
            return Error(error="IdError",
                         message="нет такого id",
                         status_code=404)
