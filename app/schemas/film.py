from pydantic import BaseModel
from datetime import datetime


class Film(BaseModel):
    id: int
    name: str
    id_img: int
    introduction_id_img: int
    conclusion_id_img: int
    places_id: list[int]
    last_modification: datetime
