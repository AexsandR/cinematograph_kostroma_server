from pydantic import BaseModel

class ImgWithAudio(BaseModel):
    id: int
    id_img: int
    id_audio: int