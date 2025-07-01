from app.db import db_session
from app.schemas.conclusion import Conclusion
from app.schemas.error import Error
from app.db.models import conclusion as db


class ApiConclusion:

    def get_conclusion(self, id: str) -> Conclusion | Error:
        db_sess = db_session.create_session()
        introduction: db.Conclusion = db_sess.query(db.Conclusion).filter(db.Conclusion.id == int(id)).first()
        if introduction is None:
            return Error(error="Id invalid",
                         message="нет такого id",
                         status_code=404)

        return Conclusion(id=int(id),
                          id_img=introduction.id_img,
                          id_audio=introduction.id_audio)
