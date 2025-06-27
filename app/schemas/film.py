from pydantic import BaseModel
from datetime import datetime

class Film(BaseModel):
    id: int
    id_img: int
    name: str
    description: str
    last_modification: datetime