from pydantic import BaseModel


class MassUpdateRequest(BaseModel):
    mass: float
