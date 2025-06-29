from http.client import HTTPResponse

from fastapi import APIRouter, UploadFile, Request, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db import db_session
from app.db.__all_models import Images, Films


class FormAdd:
    def __init__(self, ):
        self.__templates = Jinja2Templates(directory="app/templates")
        self.router = APIRouter(prefix="/addForm")
        self.router.add_api_route("/film", self.get_form_film, methods=["POST"], response_model=None)
        self.router.add_api_route("/film", self.__show_form, methods=["GET"])

    def __show_form(self, request: Request) -> HTMLResponse:
        return self.__templates.TemplateResponse("form_add_film.html", {"request": request, "error": False})

    async def get_form_film(self, request: Request, name: str = Form(...),
                            description: str = Form(...),
                            filePreview: UploadFile = File(...),
                            fileFrame: UploadFile = File(...),
                            ) -> RedirectResponse | HTTPResponse:
        print(fileFrame.filename)
        res = await self.add_preview(filePreview)
        success, id_preview = res
        res = await self.add_frame_novela(fileFrame)
        success1, id_frame = res
        success2 = await self.add_film(name, description, id_preview, id_frame)
        if success and success1 and success2:
            return RedirectResponse("/", status_code=303)
        return self.__templates.TemplateResponse("form_add_film.html",
                                                 {"request": request, "name": name, "description": description,
                                                  "error": True})

    async def add_preview(self, filePreview: UploadFile) -> tuple[bool, int]:
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

    async def add_film(self, name: str, description: str, id_preview, id_frame) -> bool:
        db_sess = db_session.create_session()
        try:
            film = Films()
            film.img_id = id_preview
            film.name = name
            film.description = description
            film.frame_id = id_frame
            db_sess.add(film)
            db_sess.commit()
            db_sess.close()
        except Exception:
            db_sess.close()
            return False
        return True

    async def add_frame_novela(self, fileFrame: UploadFile) -> tuple[bool, int]:
        db_sess = db_session.create_session()
        try:
            if fileFrame.size == 0:
                return
            frame = Images()
            file_data = await fileFrame.read()
            if isinstance(file_data, str):
                frame.bin_data = file_data.encode('latin1')  # сохраняет бинарные данные без потерь
            elif isinstance(file_data, bytes):
                frame.bin_data = file_data
            frame.type = fileFrame.content_type
            frame.is_preview = False
            db_sess.add(frame)
            db_sess.commit()
            id: int = frame.id
            db_sess.close()
        except Exception as err:
            db_sess.close()
            print(f"Ошибка в FormAdd метод add_frame_novela:\n\t{err}")
            return (False, -1)
        return (True, id)
