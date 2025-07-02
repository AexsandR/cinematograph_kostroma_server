from app.db import db_session
from app.schemas.question import Question
from app.schemas.error import Error
from app.db.models.questions import Questions
from fastapi import APIRouter


class ApiQuestions:
    def __init__(self):
        self.router = APIRouter(prefix="/api")
        self.router.add_api_route("/get_question/{id}", self.get_question, methods=["GET"])

    def get_question(self, id: str) -> Question | Error:
        db_sess = db_session.create_session()
        question: Questions = db_sess.query(Questions).filter(Questions.id == int(id)).first()
        if question is None:
            response = Error(error="Id invalid",
                             message="нет такого id",
                             status_code=404)
        else:
            response = Question(question=question.question, answer1=question.answer1,
                                answer2=question.answer2, answer3=question.answer3,
                                answer4=question.answer4)
        db_sess.close()
        return response

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
