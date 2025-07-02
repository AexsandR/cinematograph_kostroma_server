from fastapi.responses import RedirectResponse
from fastapi import APIRouter
from app.db.__all_models import *
from app.db import db_session
from app.endpoints.api_img_with_audio import ApiImgWithAudio
from app.endpoints.api_media import ApiMedia
from app.endpoints.api_questions import ApiQuestions
from app.schemas.place import Place
from app.db.models.films import Films


class ApiPlace:
    def __init__(self):
        self.routers = APIRouter(prefix="/api")
        self.routers.add_api_route("/get_place/{id_place}", self.get_place, methods=["GET"])
        self.routers.add_api_route("/get_places/{id_film}", self.get_places, methods=["GET"])
        self.routers.add_api_route("/del_place/{id_film}/{id_place}", self.del_place, methods=["GET"])
        self.__apiImgWithAudio = ApiImgWithAudio()
        self.__apiMedia = ApiMedia()
        self.__apiQuestions = ApiQuestions()

    def del_place(self, id_film: str, id_place: str) -> RedirectResponse:
        db_sess = db_session.create_session()
        place: Places = db_sess.query(Places).filter(Places.id == id_place).first()
        id_video = place.id_video
        id_orig_frame = place.id_orig_frame
        id_distorted_frame = place.id_distorted_frame
        id_question = place.id_question
        id_fact = place.fact_id
        id_frame_text = place.id_frame_text
        db_sess.delete(place)
        db_sess.commit()
        self.__apiImgWithAudio.del_img_with_audio(id_fact)
        self.__apiQuestions.del_question(id_question)
        self.__apiMedia.del_media(id_distorted_frame)
        self.__apiMedia.del_media(id_video)
        self.__apiMedia.del_media(id_orig_frame)
        self.__apiMedia.del_media(id_frame_text)
        db_sess.close()
        return RedirectResponse(f"films/place/{id_film}", status_code=303)

    def get_place(self, id_place: str) -> Place:
        db_sess = db_session.create_session()
        place = db_sess.query(Places).filter(Places.id == int(id_place)).first()
        db_sess.close()
        return Place(
            id=place.id,
            name_place=place.name_place,
            latitude=place.latitude,
            longitude=place.longitude,
            radius=place.radius,
            id_fact=place.fact_id,
            id_distorted_frame=place.id_distorted_frame,
            id_orig_frame=place.id_orig_frame,
            id_video=place.id_video,
            id_frame_text=place.id_frame_text,
            id_question=place.id_question,
            last_modification=place.last_modification
        )

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
                    latitude=place.latitude,
                    longitude=place.longitude,
                    radius=place.radius,
                    id_fact=place.fact_id,
                    id_distorted_frame=place.id_distorted_frame,
                    id_orig_frame=place.id_orig_frame,
                    id_video=place.id_video,
                    id_frame_text=place.id_frame_text,
                    id_question=place.id_question,
                    last_modification=place.last_modification
                )
            )

        db_sess.close()
        return response
