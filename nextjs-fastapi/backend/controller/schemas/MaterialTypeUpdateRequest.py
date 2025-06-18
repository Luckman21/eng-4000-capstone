from pydantic import BaseModel
from typing import Optional


class MaterialTypeUpdateRequest(BaseModel):
    type_name: Optional[str] = None
