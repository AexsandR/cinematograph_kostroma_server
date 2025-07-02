from logging import logThreads

from fastapi import APIRouter, UploadFile, Request, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db import db_session
from app.db.__all_models import Films
from app.db.models.places import Places
from app.db.models.questions import Questions
from app.schemas.question import Question
from app.endpoints.api_films import ApiFilms
from app.endpoints.api_media import ApiMedia
from app.endpoints.api_img_with_audio import ApiImgWithAudio
from app.db.models.img_with_audio import ImgWithAudio
from app.endpoints.api_place import ApiPlace
from app.schemas.place import Place
from app.endpoints.api_questions import ApiQuestions


class FormEdit:
    def __init__(self):
        self.__templates = Jinja2Templates(directory="app/templates")
        self.router = APIRouter(prefix="/editForm")
        self.router.add_api_route("/film/{id}", self.__show_form_film, methods=["GET"], response_model=None)
        self.router.add_api_route("/film/{id}", self.__get_form_film, methods=["POST"], response_model=None)
        self.router.add_api_route("/place/{id}", self.__show_form_place, methods=["GET"], response_model=None)
        self.router.add_api_route("/place/{id}", self.__get_form_place, methods=["POST"], response_model=None)
        self.__apiFilm = ApiFilms()
        self.__apiMedia = ApiMedia()
        self.__apiImgWithAudio = ApiImgWithAudio()
        self.__apiPlace = ApiPlace()
        self.__apiQuestions = ApiQuestions()

    def __show_form_place(self, request: Request, id: str) -> HTMLResponse | RedirectResponse:
        place: Place = self.__apiPlace.get_place(id)
        questions: Question = self.__apiQuestions.get_question(str(place.id_question))
        fact = self.__apiImgWithAudio.get_obj(place.id_fact)
        return self.__templates.TemplateResponse("form_edit_place.html",
                                                 {"request": request, "error": False,
                                                  "id": id,
                                                  "name_place": place.name_place,
                                                  "latitude": place.latitude,
                                                  "longitude": place.longitude,
                                                  "question": questions.question,
                                                  "answer1": questions.answer1,
                                                  "answer2": questions.answer2,
                                                  "answer3": questions.answer3,
                                                  "answer4": questions.answer4,
                                                  "id_fact_img": fact.id_img,
                                                  "id_fact_audio": fact.id_audio,
                                                  "id_distorted_frame": place.id_distorted_frame,
                                                  "id_orig_frame": place.id_orig_frame,
                                                  "id_video": place.id_video,
                                                  "id_frame_text": place.id_frame_text
                                                  })

    def __show_form_film(self, request: Request, id: str) -> HTMLResponse | RedirectResponse:
        try:
            film = self.__apiFilm.get_film(id)
            introduction: ImgWithAudio = self.__apiImgWithAudio.get_obj(str(film.id_introduction))
            conclusion: ImgWithAudio = self.__apiImgWithAudio.get_obj(str(film.id_conclusion))
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

    async def __get_form_place(self, id: str, name_place: str = Form(...),
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
                               fileFrameText: UploadFile = File(...)) -> RedirectResponse:
        res = await self.__edit_media(fileDistortedFrame)
        success, id_distorted_frame = res
        res = await self.__edit_media(fileFrame)
        success1, id_frame = res
        res = await self.__edit_media(fileVideo)
        success2, id_video = res
        res = await self.__edit_media(fileFrameText)
        success3, id_frame_text = res
        success4 = await self.__edit_place(int(id), name_place, longitude, latitude, id_distorted_frame,
                                           id_frame, id_video, id_frame_text)
        if success and success1 and success2 and success3 and success4:
            print(111111111111111)
            await self.__edit_obj(int(id), fileFact, fileAudioFact)
            await self.__edit_question(id, question, answer1, answer2, answer3, answer4)
            return RedirectResponse(f"/", status_code=303)

        print(123123123123123)
        return RedirectResponse(f"/editForm/place/{id}", status_code=404)

    async def __edit_question(self, id: int, question_text: str, answer1: str, answer2: str, answer3: str,
                              answer4: str) -> bool:
        if answer1.strip() == "" or question_text.strip() == "":
            return False
        db_sess = db_session.create_session()
        place = db_sess.query(Places).filter(Places.id == id).first()
        if place is None:
            return False
        question: Questions = db_sess.query(Questions).filter(Questions.id == id).first()
        question.question = question_text
        answers = list(filter(lambda x: x.strip() != "", [answer1, answer2, answer3, answer4]))
        answers = answers + [""] * (4 - len(answers))
        question.answer1 = answers[0]
        question.answer2 = answers[1]
        question.answer3 = answers[2]
        question.answer4 = answers[3]
        db_sess.commit()
        db_sess.close()
        return True

    async def __get_form_film(self, id: str, name: str = Form(...),
                              filePreview: UploadFile = File(...),
                              fileIntroduction: UploadFile = File(...),
                              filAudioIntroduction: UploadFile = File(...),
                              fileConclusion: UploadFile = File(...),
                              fileAudioConclusion: UploadFile = File(...)
                              ) -> RedirectResponse:

        res = await self.__edit_media(filePreview)
        success, id_preview = res
        success1 = await self.__edit_film(int(id), name, id_preview)
        if success and success1:
            db_sess = db_session.create_session()
            id_introduction = db_sess.query(Films).filter(Films.id == int(id)).first().id_introduction
            id_conclusion = db_sess.query(Films).filter(Films.id == int(id)).first().id_conclusion
            db_sess.close()
            await self.__edit_obj(id_introduction, fileIntroduction, filAudioIntroduction)
            await self.__edit_obj(id_conclusion, fileConclusion, fileAudioConclusion)
            return RedirectResponse(f"/", status_code=303)
        return RedirectResponse(f"/editForm/film/{id}", status_code=303)

    async def __edit_obj(self, id: int, img: UploadFile, audio: UploadFile) -> bool:
        res = await self.__edit_media(img)
        success, id_img = res
        res = await self.__edit_media(audio)
        success1, id_audio = res
        if success and success1:
            print(id, id_img, id_audio)
            print("Изм")
            db_sess = db_session.create_session()
            obj = db_sess.query(ImgWithAudio).filter(ImgWithAudio.id == id).first()
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

    async def __edit_place(self, id_place: int, name_place: str, longitude: float, latitude: float,
                           id_distorted_frame: int, id_frame: int, id_video: int, id_frameText: int) -> bool:
        db_sess = db_session.create_session()

        place: Places = db_sess.query(Places).filter(Places.id == id_place).first()
        if name_place.strip() != "":
            place.name_place = name_place
        place.longitude = longitude
        place.latitude = latitude
        if id_distorted_frame != -1:
            old_id = place.id_distorted_frame
            place.id_distorted_frame = id_distorted_frame
            self.__apiMedia.del_media(old_id)
        if id_frame != -1:
            old_id = place.id_orig_frame
            place.id_orig_frame = id_frame
            self.__apiMedia.del_media(old_id)
        if id_video != -1:
            old_id = place.id_video
            place.id_video = id_video
            self.__apiMedia.del_media(old_id)
        if id_frameText != -1:
            old_id = place.id_frame_text
            place.id_frame_text = id_frameText
            self.__apiMedia.del_media(old_id)
        db_sess.commit()
        db_sess.close()
        return True

    async def __edit_film(self, id: int, name, id_preview: int) -> bool:
        db_sess = db_session.create_session()
        try:
            film = db_sess.query(Films).filter(Films.id == id).first()
            if name.strip() != "":
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
