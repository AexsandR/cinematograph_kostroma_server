
from fastapi import APIRouter, UploadFile, Request, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.db import db_session
from app.db.__all_models import Images, Films, Questions, Places
from app.schemas.place import Place


class FormAdd:
    def __init__(self, ):
        self.__templates = Jinja2Templates(directory="app/templates")
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
                               fileFact: UploadFile = File(...),
                               filePreview: UploadFile = File(...),
                               fileHint1: UploadFile = File(...),
                               fileHint2: UploadFile = File(...),
                               fileHint3: UploadFile = File(...),
                               fileHint4: UploadFile = File(...)) -> RedirectResponse | HTMLResponse:
        res = await self.add_img(fileFact)
        success, id_fact = res
        res = await self.add_img(filePreview)
        success1, id_preview = res
        res = await self.add_hints([fileHint1, fileHint2, fileHint3, fileHint4])
        success2, id_hints = res
        res = await self.add_question(question, answer1, answer2, answer3, answer4)
        success3, id_question = res
        res = await  self.add_place(int(id_film), name_place, longitude, latitude, id_fact, id_preview, id_hints,
                                    id_question)
        success4 = res
        if success and success1 and success2 and success3 and success4:
            return RedirectResponse(f"/films/place/{id_film}", status_code=303)
        return self.__templates.TemplateResponse("form_add_place.html",
                                                 {"request": request, "id": id_film, "error": True})

    async def add_place(self, id_film: int, name_place: str,
                        longitude: float, latitude: float, id_fact: int, id_preview: int, id_hints: list[int],
                        id_question) -> bool:
        db_sess = db_session.create_session()
        place: Places = Places()
        place.name_place = name_place
        place.latitude = latitude
        place.longitude = longitude
        place.fact_id = id_fact
        place.img_id = id_preview
        place.id_question = id_question
        db_sess.add(place)
        db_sess.commit()
        film: Films = db_sess.query(Films).filter(Films.id == id_film).first()
        images = db_sess.query(Images).filter(Images.id.in_(id_hints)).all()
        place.hints.extend(images)
        film.places.extend([place])
        db_sess.commit()
        db_sess.close()
        return True

    async def __get_form_film(self, request: Request, name: str = Form(...),
                              description: str = Form(...),
                              filePreview: UploadFile = File(...),
                              fileFrame: UploadFile = File(...),

                              ) -> RedirectResponse | HTMLResponse:
        print(fileFrame.filename)
        res = await self.add_img(filePreview)
        success, id_preview = res
        res = await self.add_img(fileFrame)
        success1, id_frame = res
        success2 = await self.add_film(name, description, id_preview, id_frame)
        if success and success1 and success2:
            return RedirectResponse("/", status_code=303)
        return self.__templates.TemplateResponse("form_add_film.html",
                                                 {"request": request, "name": name,
                                                  "description": description,
                                                  "error": True})

    async def add_img(self, file: UploadFile) -> tuple[bool, int]:
        db_sess = db_session.create_session()
        try:
            img = Images()
            file_data = await file.read()
            img.type = file.content_type
            if isinstance(file_data, str):
                img.bin_data = file_data.encode('latin1')  # сохраняет бинарные данные без потерь
            elif isinstance(file_data, bytes):
                img.bin_data = file_data
            db_sess.add(img)
            db_sess.commit()
            id: int = img.id
            db_sess.close()
        except Exception as err:
            db_sess.close()
            print(f"Ошиибка на добавление картинки:\n\t{err}")
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

    async def add_hints(self, hints: list[UploadFile]) -> tuple[bool, list[int]]:
        id_hints: list[int] = []
        success_hint: list[bool] = []
        for hint in hints:
            res = await self.add_img(hint)
            success, id_hint = res
            id_hints.append(id_hint)
            success_hint.append(success)
        return (all(success_hint), id_hints)

    async def add_question(self, question: str, answer1: str, answer2: str, answer3: str, answer4: str) \
            -> tuple[bool, int]:
        db_sess = db_session.create_session()
        question_db: Questions = Questions()
        question_db.question = question
        question_db.answer1 = answer1
        question_db.answer2 = answer2
        question_db.answer3 = answer3
        question_db.answer4 = answer4
        db_sess.add(question_db)
        db_sess.commit()
        id: int = question_db.id
        db_sess.close()
        return (True, id)
