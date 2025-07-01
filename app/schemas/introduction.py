from pydantic import BaseModel

class Introduction(BaseModel):
    id: int
    id_img: int
    id_audio: int