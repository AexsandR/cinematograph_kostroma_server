from fastapi import APIRouter, UploadFile, Request, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db import db_session
from app.db.__all_models import Media, Films, Questions, Places
from .api_media import ApiMedia
from ..db.models.img_with_audio import ImgWithAudio
from app.endpoints.api_questions import ApiQuestions


class FormAdd:
    def __init__(self, ):
        self.__templates = Jinja2Templates(directory="app/templates")
        self.__apiMedia = ApiMedia()
        self.__apiQuestions = ApiQuestions()
        self.router = APIRouter(prefix="/addForm")
        self.router.add_api_route("/film", self.__get_form_film, methods=["POST"], response_model=None)
        self.router.add_api_route("/film", self.__show_form_film, methods=["GET"])
        self.router.add_api_route("/place/{id_film}", self.__show_form_place, methods=["GET"])
        self.router.add_api_route("/place/{id_film}", self.__get_form_place, methods=["POST"], response_model=None)

    def __show_form_film(self, request: Request) -> HTMLResponse:
        return self.__templates.TemplateResponse("form_add_film.html", {"request": request, "error": False})

    def __show_form_place(self, request: Request, id_film: str) -> HTMLResponse:
        return self.__templates.TemplateResponse("form_add_place.html",
                                                 {"request": request, "id": id_film, "error": False})

    async def __get_form_place(self, request: Request, id_film: str, name_place: str = Form(...),
                               latitude: float = Form(...),
                               longitude: float = Form(...),
                               question: str = Form(...),
                               answer1: str = Form(...),
                               answer2: str = Form(...),
                               answer3: str = Form(...),
                               answer4: str = Form(...),
                               fileAudioFact: UploadFile = Form(...),
                               fileFact: UploadFile = File(...),
                               fileDistortedFrame: UploadFile = File(...),
                               fileFrame: UploadFile = File(...),
                               fileVideo: UploadFile = File(...),
                               fileFrameText: UploadFile = File(...)) -> RedirectResponse | HTMLResponse:
        res = await self.__apiQuestions.add_question(question, answer1, answer2, answer3, answer4)
        success, id_question = res
        res = await self.__apiMedia.add_media(fileDistortedFrame)
        success1, id_distortedFrame = res
        res = await self.__apiMedia.add_media(fileFrame)
        success2, id_frame = res
        res = await self.__apiMedia.add_media(fileVideo)
        success3, id_video = res
        res = await self.__apiMedia.add_media(fileFrameText)
        success4, id_frameText = res
        res = await self.__add_img_with_audio(fileFact, fileAudioFact)
        success5, id_fact = res
        res = await  self.add_place(int(id_film), name_place, longitude, latitude, id_question, id_fact,
                                    id_distortedFrame, id_frame,
                                    id_video, id_frameText)
        success6 = res
        if success and success1 and success2 and success3 and success4 and success5 and success6:
            return RedirectResponse(f"/films/place/{id_film}", status_code=303)
        return self.__templates.TemplateResponse("form_add_place.html",
                                                 {"request": request, "id": id_film, "error": True})

    async def add_place(self, id_film: int, name_place: str,
                        longitude: float, latitude: float, id_question: int, id_fact: int, id_distorted_frame: int,
                        id_frame: int, id_video: int, id_frameText: int) -> bool:
        db_sess = db_session.create_session()
        place: Places = Places()
        place.name_place = name_place
        place.latitude = latitude
        place.longitude = longitude
        place.id_question = id_question
        place.fact_id = id_fact
        place.id_distorted_frame = id_distorted_frame
        place.id_orig_frame = id_frame
        place.id_video = id_video
        place.id_frame_text = id_frameText
        db_sess.add(place)
        db_sess.commit()
        film: Films = db_sess.query(Films).filter(Films.id == id_film).first()
        film.places.extend([place])
        db_sess.commit()
        db_sess.close()
        return True

    async def __get_form_film(self, request: Request, name: str = Form(...),
                              filePreview: UploadFile = File(...),
                              fileIntroduction: UploadFile = File(...),
                              filAudioIntroduction: UploadFile = File(...),
                              fileConclusion: UploadFile = File(...),
                              fileAudioConclusion: UploadFile = File(...)
                              ) -> RedirectResponse | HTMLResponse:
        res = await self.__apiMedia.add_media(filePreview)
        success, id_preview = res
        res = await self.__add_img_with_audio(fileIntroduction, filAudioIntroduction)
        success1, id_introduction = res
        res = await self.__add_img_with_audio(fileConclusion, fileAudioConclusion)
        success2, id_conclusion = res
        success3 = await self.add_film(name, id_preview, id_introduction, id_conclusion)
        if success and success1 and success2 and success3:
            return RedirectResponse("/", status_code=303)
        return self.__templates.TemplateResponse("form_add_film.html",
                                                 {"request": request, "name": name,
                                                  "error": True})

    async def __add_img_with_audio(self, file: UploadFile, audio: UploadFile) -> tuple[bool, int]:
        res = await self.__apiMedia.add_media(file)
        success, id_media_img = res
        res = await self.__apiMedia.add_media(audio)
        success1, id_media_audio = res
        if success and success1:
            db_sess = db_session.create_session()
            try:
                imgWithAudio = ImgWithAudio()
                imgWithAudio.id_img = id_media_img
                imgWithAudio.id_audio = id_media_audio
                db_sess.add(imgWithAudio)
                db_sess.commit()
                id: int = imgWithAudio.id
                db_sess.close()
                return (True, id)
            except Exception as err:
                print(f"Ошибка при добавлении imgWithAudio:\n\t{err}")
                db_sess.close()
        if success:
            self.__apiMedia.del_media(id_media_img)
        if success1:
            self.__apiMedia.del_media(id_media_audio)
        return (False, -1)

    async def add_film(self, name: str, id_preview: int, id_introduction: int, id_conclusion: int) -> bool:
        db_sess = db_session.create_session()
        try:
            film = Films()
            film.img_id = id_preview
            film.name = name
            film.id_introduction = id_introduction
            film.id_conclusion = id_conclusion
            db_sess.add(film)
            db_sess.commit()
            db_sess.close()
        except Exception:
            db_sess.close()
            return False
        return True
