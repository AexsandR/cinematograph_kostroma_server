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
                                                      "name": film.name,
                                                      "id_img": film.id_img,
                                                      "introduction_id_img": film.introduction_id_img,
                                                      "conclusion_id_img": film.conclusion_id_img,
                                                      })
        except Exception as err:
            print(f"Ошибка в показе форме на изменеия фильма:\n\t{err}")
            return RedirectResponse("/", status_code=303)

    async def __get_form_film(self, request: Request, id: str, name: str = Form(...),
                              filePreview: UploadFile = File(...),
                              fileIntroduction: UploadFile = File(...),
                              fileConclusion: UploadFile = File(...),
                              ) -> RedirectResponse | HTMLResponse:
        res = await self.__edit_img(filePreview)
        success, id_preview = res
        res = await self.__edit_img(fileIntroduction)
        success1, id_introduction = res
        res = await self.__edit_img(fileConclusion)
        success2, id_conclusion = res
        success3 = await self.__efit_film(int(id), name, id_preview, id_introduction, id_conclusion)
        if success and success1 and success2 and success3:
            return RedirectResponse("/", status_code=303)
        film = self.__apiFilm.get_film(id)
        if success:
            self.__apiImages.del_img(id_preview)
        if success1:
            self.__apiImages.del_img(id_introduction)
        if success2:
            self.__apiImages.del_img(id_conclusion)
        return self.__templates.TemplateResponse("edit_form_film.html",
                                                 {"request": request, "error": False, "type": "film",
                                                  "id": id,
                                                  "name": film.name,
                                                  "id_img": film.id_img,
                                                  "introduction_id_img": film.introduction_id_img,
                                                  "conclusion_id_img": film.conclusion_id_img,
                                                  })

    async def __edit_img(self, filePreview: UploadFile) -> tuple[bool, int]:
        if filePreview.size == 0:
            return (True, -1)
        res = await self.__addForm.add_img(filePreview)
        return res

    async def __efit_film(self, id: int, name: str, id_preview: int, id_introduction: int,
                          id_conclusion: int, ) -> bool:
        db_sess = db_session.create_session()
        print(id_introduction)
        print(id_conclusion)

        try:
            film = db_sess.query(Films).filter(Films.id == id).first()
            film.name = name
            if id_preview != -1:
                old_id_preview: int = film.img_id
                film.img_id = id_preview
                self.__apiImages.del_img(old_id_preview)
            if id_introduction != -1:
                old_id_introduction: int = film.introduction_id_img
                print(id_introduction)
                film.introduction_id_img = id_introduction
                self.__apiImages.del_img(old_id_introduction)
            if id_conclusion != -1:
                old_id_conclusion: int = film.conclusion_id_img
                film.conclusion_id_img = id_conclusion
                self.__apiImages.del_img(old_id_conclusion)

            db_sess.commit()
            db_sess.close()
            return True
        except Exception as err:
            db_sess.close()
            print(f"Ошибка в измении фильма:\n\t{err}")
            return False
