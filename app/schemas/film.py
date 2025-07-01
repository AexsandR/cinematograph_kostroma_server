from pydantic import BaseModel
from datetime import datetime


class Film(BaseModel):
    id: int
    name: str
    id_img: int
    id_introduction: int
    id_conclusion: int
    id_places: list[int]
    last_modification: datetime
