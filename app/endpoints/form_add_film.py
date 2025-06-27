from fastapi import APIRouter, UploadFile, Request, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db import db_session
from app.db.__all_models import Images, Films, FrameNovela


class FormAddFilm:
    def __init__(self, ):
        self.__templates = Jinja2Templates(directory="app/templates")
        self.router = APIRouter(prefix="/add_film")
        self.router.add_api_route("/", self.__get_form_film, methods=["POST"])
        self.router.add_api_route("/", self.__show_form, methods=["GET"])

    def __show_form(self, request: Request) -> HTMLResponse:
        return self.__templates.TemplateResponse("form_add_film.html", {"request": request})

    async def __get_form_film(self, name: str = Form(...),
                              description: str = Form(...),
                              filePreview: UploadFile = File(...),
                              fileFrames: list[UploadFile] = File(...)) -> RedirectResponse:
        print(name, description)
        id_preview = await self.__add_preview(filePreview)
        print(f"------------\n{id_preview}")
        id_film = await self.__add_film(name, description, id_preview)
        await self.__add_frame_novela(fileFrames, id_film)
        return RedirectResponse("/", status_code=303)

    async def __add_preview(self, filePreview: UploadFile) -> int:
        db_sess = db_session.create_session()
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
        return id

    async def __add_film(self, name: str, description: str, id_preview) -> int:
        print(name, description, id_preview)
        film = Films()
        film.img_id = id_preview
        film.name = name
        film.description = description
        db_sess = db_session.create_session()
        db_sess.add(film)
        db_sess.commit()
        id = film.id
        db_sess.close()
        return id

    async def __add_frame_novela(self, fileFrames: list[UploadFile], id_film: int) -> None:
        db_sess = db_session.create_session()
        for fileFrame in fileFrames:
            frame = FrameNovela()
            file_data = await fileFrame.read()
            if isinstance(file_data, str):
                frame.bin_data = file_data.encode('latin1')  # сохраняет бинарные данные без потерь
            elif isinstance(file_data, bytes):
                frame.bin_data = file_data
            frame.type = fileFrame.content_type
            frame.id_film = id_film
            db_sess.add(frame)
        db_sess.commit()
        db_sess.close()

# FormData(
#     [
#         ('name', 'erwerwer'),
#         ('description', 'werwerwer'),
#         ('filePreview', UploadFile(filename='2025-06-25-023316_hyprshot.png', size=16451, headers=Headers({'content-disposition': 'form-data; name="filePreview"; filename="2025-06-25-023316_hyprshot.png"', 'content-type': 'image/png'}))),
#         ('fileFrames', UploadFile(filename='2025-06-25-174907_hyprshot.png', size=167300, headers=Headers({'content-disposition': 'form-data; name="fileFrames"; filename="2025-06-25-174907_hyprshot.png"', 'content-type': 'image/png'})))
#     ]
# )
