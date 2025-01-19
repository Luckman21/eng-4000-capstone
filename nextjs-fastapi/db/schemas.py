from pydantic import BaseModel

class MaterialSchema(BaseModel):
    id: int
    colour: str
    supplier_link: str
    mass: float
    material_type_id: int
    shelf_id: int

    class Config:
        orm_mode = True

class MaterialTypeSchema(BaseModel):
    id: int
    type_name: str

    class Config:
        orm_mode = True
class UserSchema(BaseModel):
    id: int
    username: str
    password: str
    email: str
    user_type_id: int

    class Config:
        orm_mode = True

