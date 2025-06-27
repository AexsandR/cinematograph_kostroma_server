from pydantic import BaseModel
from datetime import datetime
from typing import Annotated
from pydantic.types import StringConstraints

class PlaceResponse(BaseModel):
    id: int
    name_place: Annotated[str, StringConstraints(max_length=300)]
    description: Annotated[str, StringConstraints(max_length=500)]
    latitude: float
    longitude: float
    radius: float
    img_id: int
    last_modification: datetime = datetime.now()
    
class ImageResponse(BaseModel):
    id: int
    img: bytes


