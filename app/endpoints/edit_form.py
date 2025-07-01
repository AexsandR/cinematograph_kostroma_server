from fastapi import APIRouter, UploadFile, Request, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db import db_session
from app.db.__all_models import Films
from app.db.models.conclusion import Conclusion
from app.endpoints.api_films import ApiFilms
from app.endpoints.form_add import FormAdd
from app.endpoints.api_media import ApiMedia
from app.endpoints.api_introduction import ApiIntroduction
from app.endpoints.api_conclusion import ApiConclusion
from app.db.models.introduction import Introduction
from app.db.models.conclusion import Conclusion


class FormEdit:
    def __init__(self):
        self.__templates = Jinja2Templates(directory="app/templates")
        self.router = APIRouter(prefix="/editForm")
        self.router.add_api_route("/film/{id}", self.__show_form_film, methods=["GET"], response_model=None)
        self.router.add_api_route("/film/{id}", self.__get_form_film, methods=["POST"], response_model=None)
        self.__apiFilm = ApiFilms()
        self.__addForm = FormAdd()
        self.__apiMedia = ApiMedia()
        self.__apiIntroduction = ApiIntroduction()
        self.__apiConclusion = ApiConclusion()

    def __show_form_film(self, request: Request, id: str) -> HTMLResponse | RedirectResponse:
        try:
            film = self.__apiFilm.get_film(id)
            introduction: Introduction = self.__apiIntroduction.get_introduction(str(film.id_introduction))
            conclusion: Conclusion = self.__apiConclusion.get_conclusion(str(film.id_conclusion))
            return self.__templates.TemplateResponse("edit_form_film.html",
                                                     {"request": request, "error": False, "type": "film",
                                                      "id": id,
                                                      "name": film.name,
                                                      "id_img": film.id_img,
                                                      "introduction_id_img": introduction.id_img,
                                                      "introduction_id_audio": introduction.id_audio,
                                                      "conclusion_id_img": conclusion.id_img,
                                                      "conclusion_id_audio": conclusion.id_audio,
                                                      })
        except Exception as err:
            print(f"Ошибка в показе форме на изменеия фильма:\n\t{err}")
            return RedirectResponse("/", status_code=303)

    async def __get_form_film(self, request: Request, id: str, name: str = Form(...),
                              filePreview: UploadFile = File(...),
                              fileIntroduction: UploadFile = File(...),
                              filAudioIntroduction: UploadFile = File(...),
                              fileConclusion: UploadFile = File(...),
                              fileAudioConclusion: UploadFile = File(...)
                              ) -> RedirectResponse | HTMLResponse:
        res = await self.__edit_media(filePreview)
        print(res)
        success, id_preview = res
        success1 = await self.__efit_film(int(id), name, id_preview)
        if success and success1:
            await self.edit_introduction_conclusion(int(id), Introduction, fileIntroduction, filAudioIntroduction)
            await self.edit_introduction_conclusion(int(id), Conclusion, fileConclusion, fileAudioConclusion)
            return RedirectResponse(f"/", status_code=303)
        print(success)
        print(success1)
        return RedirectResponse(f"/editForm/film/{id}", status_code=303)

    async def edit_introduction_conclusion(self, id: int, Class, img: UploadFile, audio: UploadFile) -> bool:
        res = await self.__edit_media(img)
        success, id_img = res
        res = await self.__edit_media(audio)
        success1, id_audio = res
        if success and success1:
            db_sess = db_session.create_session()
            obj = db_sess.query(Class).filter(Class.id == id).first()
            print(id_img, id_audio)
            if id_img != -1:
                old_id = obj.id_img
                obj.id_img = id_img
                self.__apiMedia.del_media(old_id)
            if id_audio != -1:
                old_id = obj.id_audio
                obj.id_audio = id_audio
                self.__apiMedia.del_media(old_id)
            db_sess.commit()
            db_sess.close()

    async def __edit_media(self, file: UploadFile) -> tuple[bool, int]:
        if file.size == 0:
            return (True, -1)
        res = await self.__apiMedia.add_media(file)
        return res

    async def __efit_film(self, id: int, name, id_preview: int) -> bool:
        db_sess = db_session.create_session()
        try:
            film = db_sess.query(Films).filter(Films.id == id).first()
            film.name = name
            if id_preview != -1:
                old_id_preview: int = film.img_id
                film.img_id = id_preview
                self.__apiMedia.del_media(old_id_preview)
            db_sess.commit()
            db_sess.close()
            return True
        except Exception as err:
            db_sess.close()
            print(f"Ошибка в измении фильма:\n\t{err}")
            return False
