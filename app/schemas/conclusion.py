from pydantic import BaseModel


class Conclusion(BaseModel):
    id: int
    id_img: int
    id_audio: int
