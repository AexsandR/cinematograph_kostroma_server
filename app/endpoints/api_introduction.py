from app.db import db_session
from app.schemas.introduction import Introduction
from app.schemas.error import Error
from app.db.models import introduction as db


class ApiIntroduction:

    def get_introduction(self, id: str) -> Introduction | Error:
        db_sess = db_session.create_session()
        introduction: db.Introduction = db_sess.query(db.Introduction).filter(db.Introduction.id == int(id)).first()
        if introduction is None:
            return Error(error="Id invalid",
                         message="нет такого id",
                         status_code=404)

        return Introduction(id=int(id),
                            id_img=introduction.id_img,
                            id_audio=introduction.id_audio)
