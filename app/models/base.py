from pydantic import BaseModel
from typing import Optional, Dict, Any


class ResponseModel(BaseModel):
    detail: str
    data: Optional[Dict[str, Any]]
