from app.db import db_session
from app.schemas.img_with_audio import ImgWithAudio
from app.schemas.error import Error
from app.db.models import img_with_audio as db


class ApiImgWithAudio:

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
