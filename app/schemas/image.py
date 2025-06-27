from pydantic import BaseModel
import base64

class Image(BaseModel):
    type: str
    bin_data: str

