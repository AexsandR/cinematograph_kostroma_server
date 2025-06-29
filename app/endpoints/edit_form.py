import json
from fastapi import APIRouter, UploadFile, Request, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db import db_session
from app.db.__all_models import Films
from app.endpoints.api_films import ApiFilms
from app.endpoints.form_add import FormAdd
from app.endpoints.api_image import ApiImages


class FormEdit:
    def __init__(self):
        self.__templates = Jinja2Templates(directory="app/templates")
        self.router = APIRouter(prefix="/editForm")
        self.router.add_api_route("/film/{id}", self.__show_form_film, methods=["GET"], response_model=None)
        self.router.add_api_route("/film/{id}", self.__get_form_film, methods=["POST"], response_model=None)
        self.__apiFilm = ApiFilms()
        self.__addForm = FormAdd()
        self.__apiImages = ApiImages()

    def __show_form_film(self, request: Request, id: str) -> HTMLResponse | RedirectResponse:
        try:
            film = self.__apiFilm.get_film(id)
            return self.__templates.TemplateResponse("edit_form_film.html",
                                                     {"request": request, "error": False, "type": "film",
                                                      "id": id,
                                                      "name": film.name, "description": film.description,
                                                      "id_img": film.id_img,
                                                      "id_frame": film.id_frame
                                                      })
        except Exception as err:
            print(f"Ошибка в показе форме на изменеия фильма:\n\t{err}")
            return RedirectResponse("/", status_code=303)

    async def __get_form_film(self, request: Request,
                              id: str, name: str = Form(...),
                              description: str = Form(...),
                              filePreview: UploadFile = File(...),
                              fileFrame: UploadFile = File(...),
                              ) -> RedirectResponse | HTMLResponse:
        res = await self.__edit_preview(filePreview)
        success, id_preview = res
        res = await self.__edit_frame(fileFrame)
        success1, id_frame = res
        success2 = await self.__efit_film(int(id), name, description, id_preview, id_frame)
        if success and success1 and success2:
            return RedirectResponse("/", status_code=303)

        return self.__templates.TemplateResponse("edit_form_film.html",
                                                 {"request": request, "error": False, "type": "film",
                                                  "name": name, "description": description,
                                                  "id_img": id_preview,
                                                  "id_frame": id_frame
                                                  })

    async def __edit_preview(self, filePreview: UploadFile) -> tuple[bool, int]:
        if filePreview.size == 0:
            return (True, -1)
        res = await self.__addForm.add_preview(filePreview)
        return res

    async def __edit_frame(self, fileFrame: UploadFile) -> tuple[bool, int]:
        if fileFrame.size == 0:
            return (True, -1)
        res = await self.__addForm.add_frame_novela(fileFrame)
        return res

    async def __efit_film(self, id: int, name: str, description: str, id_preview: int, id_frame: int) -> bool:
        db_sess = db_session.create_session()
        old_id_frame: int = -1
        old_id_preview: int = -1
        try:
            film = db_sess.query(Films).filter(Films.id == id).first()
            film.name = name
            film.description = description
            if id_frame != -1:
                old_id_frame = film.frame_id
                film.frame_id = id_frame
                self.__apiFramesNovela.del_img(old_id_frame)

            if id_preview != -1:
                old_id_preview = film.img_id
                film.img_id = id_preview
                self.__apiImages.del_img(old_id_preview)
            db_sess.commit()
            db_sess.close()
            return True
        except Exception as err:
            db_sess.close()
            print(f"Ошибка в измении фильма:\n\t{err}")
            return False
