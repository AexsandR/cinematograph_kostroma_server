from http.client import HTTPException
from app.db import db_session
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import Response, JSONResponse
from app.db.__all_models import *
from datetime import datetime
from email.utils import formatdate


class ApiMedia:
    def __init__(self):
        self.routres = APIRouter(prefix="/api")
        self.routres.add_api_route("/get_media/{id_media}", self.__get_media, methods=["GET"])

    def __get_media_bin(self, id_image: int) -> tuple[str, bytes]:
        db_sess = db_session.create_session()
        img: Media = db_sess.query(Media).filter(Media.id == id_image).first()
        db_sess.close()
        if img:
            return (img.type, img.bin_data)
        else:
            return ("", b"")

    def del_media(self, id: int) -> JSONResponse:
        db_sess = db_session.create_session()
        media = db_sess.query(Media).filter(Media.id == id).first()
        if media == None:
            return JSONResponse({"status": "404"})
        db_sess.delete(media)
        db_sess.commit()
        db_sess.close()
        return JSONResponse({"status": "200"})

    def __get_media(self, id_media: str) -> Response:
        try:
            media_type, bin_data = self.__get_media_bin(int(id_media))

            if not media_type or not bin_data:
                raise HTTPException(status_code=404, detail="Нет такого id")

            # Генерируем уникальный хеш содержимого
            import hashlib
            content_hash = hashlib.md5(bin_data).hexdigest()
            last_modified = formatdate(timeval=None, localtime=False, usegmt=True)
            headers = {
                'Content-Length': str(len(bin_data)),
                'Cache-Control': 'public, max-age=604800',  # 7 дней
                'ETag': content_hash,  # Уникальный идентификатор содержимого
                'Last-Modified': last_modified  # Замените на реальную дату модификации
            }

            if media_type.startswith('video/'):
                headers.update({
                    'Accept-Ranges': 'bytes',
                    'Content-Disposition': 'inline'
                })
            elif media_type.startswith('image/'):
                ext = media_type.split('/')[-1]
                headers.update({
                    'Content-Disposition': f'inline; filename="image_{id_media}.{ext}"',
                    'Cache-Control': 'no-cache'  # Для изображений отключаем кеш
                })

            return Response(
                content=bin_data,
                media_type=media_type,
                headers=headers
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Нет такого id")

    async def add_media(self, file: UploadFile) -> tuple[bool, int]:
        db_sess = db_session.create_session()
        try:
            media = Media()
            file_data = await file.read()
            media.type = file.content_type
            if isinstance(file_data, str):
                media.bin_data = file_data.encode('latin1')  # сохраняет бинарные данные без потерь
            elif isinstance(file_data, bytes):
                media.bin_data = file_data
            db_sess.add(media)
            db_sess.commit()
            id: int = media.id
            db_sess.close()
        except Exception as err:
            db_sess.close()
            print(f"Ошиибка на добавление картинки:\n\t{err}")
            return (False, -1)
        return (True, id)
