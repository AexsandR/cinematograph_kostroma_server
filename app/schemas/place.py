from pydantic import BaseModel
from datetime import datetime
from typing import Annotated
from pydantic.types import StringConstraints


class Place(BaseModel):
    id: int
    name_place: Annotated[str, StringConstraints(max_length=300)]
    id_question: int
    latitude: float
    longitude: float
    radius: float
    id_fact: int
    id_distorted_frame: int
    id_orig_frame: int
    id_video: int
    id_frame_text: int
    id_question: int
    last_modification: datetime = datetime.now()
