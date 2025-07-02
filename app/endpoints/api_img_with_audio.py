from app.db import db_session
from app.schemas.img_with_audio import ImgWithAudio
from app.schemas.error import Error
from app.db.models import img_with_audio as db
from fastapi import APIRouter
from .api_media import ApiMedia


class ApiImgWithAudio:
    def __init__(self):
        self.__apiMedia = ApiMedia()
        self.router = APIRouter(prefix="/api")
        self.router.add_api_route("/get_img_with_audio/{id}", self.get_obj, methods=["GET"])

    def get_obj(self, id: str) -> ImgWithAudio | Error:
        db_sess = db_session.create_session()
        introduction: db.ImgWithAudio = db_sess.query(db.ImgWithAudio).filter(db.ImgWithAudio.id == int(id)).first()
        if introduction is None:
            response = Error(error="Id invalid",
                             message="нет такого id",
                             status_code=404)
        else:
            response = ImgWithAudio(id=int(id),
                                    id_img=introduction.id_img,
                                    id_audio=introduction.id_audio)
        db_sess.close()
        return response

    def del_img_with_audio(self, id: int) -> None:
        db_sess = db_session.create_session()
        obj = db_sess.query(db.ImgWithAudio).filter(db.ImgWithAudio.id == id).first()

        if obj:
            id_img: int = obj.id_img
            id_audio: int = obj.id_audio
            db_sess.delete(obj)
            db_sess.commit()
            self.__apiMedia.del_media(id_img)
            self.__apiMedia.del_media(id_audio)
        db_sess.close()
