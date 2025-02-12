from pydantic import BaseModel
from typing import Optional

class MaterialMutationRequest(BaseModel):
    mass_change: float