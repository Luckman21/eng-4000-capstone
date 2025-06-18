from pydantic import BaseModel


class MaterialTypeCreateRequest(BaseModel):
    type_name: str