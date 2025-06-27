from pydantic import BaseModel
from typing import Optional

class Error(BaseModel):
    error: str
    message: str
    detail: Optional[dict]
    status_code: int