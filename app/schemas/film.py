from pydantic import BaseModel
from datetime import datetime

class Film(BaseModel):
    id: int
    id_img: int
    id_frame: int
    name: str
    description: str
    last_modification: datetime