from http.client import HTTPResponse

from fastapi import APIRouter, UploadFile, Request, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db import db_session
from app.db.__all_models import Images, Films, FramesNovela


class FormAdd:
    def __init__(self, ):
        self.__templates = Jinja2Templates(directory="app/templates")
        self.router = APIRouter(prefix="/addForm")
        self.router.add_api_route("/film", self.__get_form_film, methods=["POST"], response_model=None)
        self.router.add_api_route("/film", self.__show_form, methods=["GET"])

    def __show_form(self, request: Request) -> HTMLResponse:
        return self.__templates.TemplateResponse("form_add_film.html", {"request": request, "error": False})

    async def __get_form_film(self, request: Request, name: str = Form(...),
                              description: str = Form(...),
                              filePreview: UploadFile = File(...),
                              fileFrame1: UploadFile = File(...),
                              fileFrame2: UploadFile = File(...),
                              fileFrame3: UploadFile = File(...)
                              ) -> RedirectResponse | HTTPResponse:
        fileFrames = [fileFrame1, fileFrame2, fileFrame3]
        print(fileFrame1.filename)
        res = await self.__add_preview(filePreview)
        success, id_preview = res
        res = await self.__add_film(name, description, id_preview)
        success1, id_film = res
        await self.__add_frame_novela(fileFrames, id_film)
        if success and success1:
            return RedirectResponse("/", status_code=303)
        return self.__templates.TemplateResponse("form_add_film.html",
                                                 {"request": request, "name": name, "description": description,
                                                  "error": True})

    async def __add_preview(self, filePreview: UploadFile) -> tuple[bool, int]:
        db_sess = db_session.create_session()
        try:
            img = Images()
            file_data = await filePreview.read()
            img.type = filePreview.content_type
            if isinstance(file_data, str):
                img.bin_data = file_data.encode('latin1')  # сохраняет бинарные данные без потерь
            elif isinstance(file_data, bytes):
                img.bin_data = file_data
            db_sess.add(img)
            db_sess.commit()
            id: int = img.id
            db_sess.close()
        except Exception:
            db_sess.close()
            return (False, -1)
        return (True, id)

    async def __add_film(self, name: str, description: str, id_preview) -> tuple[bool, int]:
        db_sess = db_session.create_session()
        try:
            film = Films()
            film.img_id = id_preview
            film.name = name
            film.description = description
            db_sess.add(film)
            db_sess.commit()
            id = film.id
            db_sess.close()
        except Exception:
            db_sess.close()
            return (False, -1)
        return (True, id)

    async def __add_frame_novela(self, fileFrames: list[UploadFile], id_film: int) -> None:
        db_sess = db_session.create_session()
        i: int = 0
        try:
            for fileFrame in fileFrames:
                if fileFrame.size == 0:
                    continue
                frame = FramesNovela()
                file_data = await fileFrame.read()
                if isinstance(file_data, str):
                    frame.bin_data = file_data.encode('latin1')  # сохраняет бинарные данные без потерь
                elif isinstance(file_data, bytes):
                    frame.bin_data = file_data
                frame.type = fileFrame.content_type
                frame.id_film = id_film
                frame.order = i
                i += 1
                db_sess.add(frame)
            db_sess.commit()
        except Exception:
            ...
        db_sess.close()
