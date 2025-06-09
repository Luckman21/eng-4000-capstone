from pydantic import BaseModel


class MaterialMutationRequest(BaseModel):
    mass_change: float