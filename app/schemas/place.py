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
    img_id: int
    fact_id: int
    hints_id: list[int]
    last_modification: datetime = datetime.now()
