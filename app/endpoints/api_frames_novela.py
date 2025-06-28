from pprint import pprint

from app.schemas.image import Image
from app.schemas.error import Error
from app.db import db_session
from fastapi import APIRouter
from fastapi.responses import Response, JSONResponse
import base64
from app.db.__all_models import FramesNovela, Films


class ApiFramesNovela:
    def __init__(self):
        self.routres = APIRouter(prefix="/api")
        self.routres.add_api_route("/get_frame/{id_image}", self.__get_frame, methods=["GET"])
        self.routres.add_api_route("/__get_ids_novela_frames/{id_film}",
                                   self.__get_ids_novela_frames, methods=["GET"])

    """надо было делать наслежование"""

    def __get_frame_bin(self, id_frame: int) -> tuple[str, bytes]:
        db_sess = db_session.create_session()
        frame: FramesNovela = db_sess.query(FramesNovela).filter(FramesNovela.id == id_frame).first()
        db_sess.close()
        if frame:
            return (frame.type, frame.bin_data)
        else:
            return ("", b"")

    def __get_frame(self, id_image: str) -> Response:
        type_img, bin_data = self.__get_frame_bin(int(id_image))
        return Response(content=bin_data, media_type=type_img)

    """возвращает все id кадров новелы у фильма"""

    def __get_ids_novela_frames(self, id_film: str) -> JSONResponse:
        db_sess = db_session.create_session()
        ids_frame: list[int] = []
        try:
            ids_frame = [frame.id for frame in
                         db_sess.query(FramesNovela).filter(FramesNovela.id_film == int(id_film)).all()]
        except Exception as err:
            print("Ошибка в ApiImages: ")
            print(f"\t{err}")
        db_sess.close()
        return JSONResponse({"ids": ids_frame})
