from pydantic import BaseModel
from typing import Optional

class MassUpdateRequest(BaseModel):
    mass: Optional[float] = None
