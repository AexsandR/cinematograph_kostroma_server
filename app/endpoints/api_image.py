from pprint import pprint

from app.schemas.image import Image
from app.schemas.error import Error
from app.db import db_session
from fastapi import APIRouter
from fastapi.responses import Response
import base64
from app.db.__all_models import *


class ApiImages:
    def __init__(self):
        self.routres = APIRouter(prefix="/api")
        self.routres.add_api_route("/get_images/{id_image}", self.__get_image, methods=["GET"])

    def __get_img_bin(self, id_image: int) -> tuple[str, bytes]:
        db_sess = db_session.create_session()
        img: Images = db_sess.query(Images).filter(Images.id == id_image).first()
        db_sess.close()
        if img:
            return (img.type, img.bin_data)
        else:
            return ("", b"")



    def __get_image(self, id_image: str) -> Response:
        type_img, bin_data = self.__get_img_bin(int(id_image))
        return Response(content=bin_data, media_type=type_img)
