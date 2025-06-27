from pprint import pprint

from app.schemas.image import Image
from app.schemas.error import Error
from app.db import db_session
from fastapi import APIRouter
from fastapi.responses import Response
import base64
from app.db.__all_models import *


class ApiImage:
    def __init__(self):
        self.routres = APIRouter(prefix="/api/get_images")
        self.routres.add_api_route("/{id_image}", self.__get_image, methods=["GET"])

    def __get_img(self, id_image: int) -> tuple[str, bytes]:
        db_sess = db_session.create_session()
        img: Images = db_sess.query(Images).filter(Images.id == id_image).first()
        db_sess.close()
        if img:
            return (img.type, img.bin_data)
        else:
            return ("", b"")



    def __get_image(self, id_image: str) -> Response:
        type_img, bin_data = self.__get_img(int(id_image))
        base64_image = base64.b64encode(bin_data).decode("latin-1")
        return Response(content=bin_data, media_type=type_img)
