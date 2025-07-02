from pydantic import BaseModel


class Question(BaseModel):
    question: str
    answer1: str
    answer2: str
    answer3: str
    answer4: str
