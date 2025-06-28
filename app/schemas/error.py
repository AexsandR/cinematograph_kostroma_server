from pydantic import BaseModel
from typing import Optional

class Error(BaseModel):
    error: str
    message: str
    status_code: int