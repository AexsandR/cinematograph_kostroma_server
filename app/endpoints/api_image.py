from http.client import HTTPException
from pprint import pprint

from app.schemas.image import Image
from app.schemas.error import Error
from app.db import db_session
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, JSONResponse
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

    def del_img(self, id: int) -> JSONResponse:
        db_sess = db_session.create_session()
        img = db_sess.query(Images).filter(Images.id == id).first()
        if img == None:
            return JSONResponse({"status": "404"})
        db_sess.delete(img)
        db_sess.commit()
        db_sess.close()
        return JSONResponse({"status": "200"})

    def __get_image(self, id_image: str) -> Response:
        try:
            media_type, bin_data = self.__get_img_bin(int(id_image))

            if not media_type or not bin_data:
                raise HTTPException(status_code=404, detail="Нет такого id")

            headers = {
                'Content-Length': str(len(bin_data)),
                'Cache-Control': 'public, max-age=86400',
            }

            if media_type.startswith('video/'):
                headers.update({
                    'Accept-Ranges': 'bytes',
                    'Content-Disposition': 'inline'
                })
            elif media_type.startswith('image/'):
                headers['Content-Disposition'] = f'inline; filename="image_{id_image}.{media_type.split('/')[-1]}"'

            return Response(
                content=bin_data,
                media_type=media_type,
                headers=headers
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Нет такого id")
