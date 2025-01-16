import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent.parent))
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.controller.dependencies import get_db
from db.schemas import MaterialSchema 
from db.model.Material import Material
from db.model.User import User
from db.model.MaterialType import MaterialType
from db.model.UserType import UserType
from fastapi.middleware.cors import CORSMiddleware
from db.repositories.MaterialRepository import MaterialRepository
from db.repositories.UserRepository import UserRepository
import asyncio
from sqlalchemy import event
from backend.controller import listener
from backend.controller.schemas.MaterialUpdateRequest import MaterialUpdateRequest
from backend.controller.schemas.MaterialCreateRequest import MaterialCreateRequest
from db.repositories.MaterialTypeRepository import MaterialTypeRepository
from backend.controller.schemas.UserUpdateRequest import UserUpdateRequest
from backend.controller.schemas.UserCreateRequest import UserCreateRequest
from backend.controller.schemas.MaterialTypeUpdateRequest import MaterialTypeUpdateRequest
from backend.controller.schemas.MaterialTypeCreateRequest import MaterialTypeCreateRequest

app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up listeners on startup
@app.on_event("startup")
def setup_listeners():
    low_stock_listener()

# Create a listener that triggers when the Material table is updated, checks for Materials with a mass below the threshold
def low_stock_listener():
    def listener_wrapper(mapper, connection, target):
        asyncio.create_task(listener.job_complete_listener(mapper, connection, target))

    event.listen(Material, 'after_update', listener_wrapper)

# Now define your API routes
@app.get("/materials", response_model=list[MaterialSchema])
async def get_Allmaterials(db: Session = Depends(get_db)):
    repo = MaterialRepository(db)
    return repo.get_all_materials()

@app.get("/material_types")
async def get_all_material_types(db: Session = Depends(get_db)):
    repo =MaterialTypeRepository(db)
    return repo.get_all_material_types()

@app.get("/users")
async def get_all_users(db: Session = Depends(get_db)):
    repo =UserRepository(db)
    return repo.get_all_users()

@app.post("/create_material")
async def create_material(request: MaterialCreateRequest, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)

    material = db.query(Material).filter_by(name=request.name, colour=request.colour, material_type_id=request.material_type_id).first()

    # Check if the entity exists
    if material is not None and repo.material_exists(material.id):
        raise HTTPException(status_code=404, detail="Material already exists")

    # Call the update method

    try:
        # Call the setter method to update the material
        repo.create_material(
                             colour=request.colour,
                             name=request.name,
                             mass=request.mass,
                             material_type_id=request.material_type_id,
                             shelf_id=request.shelf_id
                             )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material successfully created"}




@app.delete("/delete_material/{entity_id}")
async def delete_material(entity_id: int, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)

    # Check if the entity exists
    if not repo.material_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material not found")

    # Call the update method
    material = repo.get_material_by_id(entity_id)

    try:
        # Call the setter method to update the material
        repo.delete_material(material)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    material = repo.get_material_by_id(entity_id)

    return {'message': "Material deleted successfully"}

@app.put("/update_material/{entity_id}")
async def update_material(entity_id: int, request: MaterialUpdateRequest, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)
    # Check if the entity exists
    if not repo.material_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material not found")

    # Call the update method
    material = repo.get_material_by_id(entity_id)
    try:
        # Call the setter method to update the material
        repo.update_material(material,
                             mass=request.mass,
                             colour=request.colour,
                             material_type_id=request.material_type_id,
                             name=request.name,
                             shelf_id = request.shelf_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material updated successfully"}


@app.post("/create_user")
async def create_user(request: UserCreateRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)

    user = db.query(User).filter_by(email=request.email, username=request.username, user_type_id=request.user_type_id).first()

    # Check if the entity exists
    if user is not None and repo.user_exists(user.id):
        raise HTTPException(status_code=404, detail="User already exists")

    # Call the update method

    try:
        # Call the setter method to update the material
        repo.create_user(
                             username=request.username,
                             user_type_id=request.user_type_id,
                             password=request.password,
                             email=request.email
                             )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "User successfully created"}




@app.delete("/delete_user/{entity_id}")
async def delete_user(entity_id: int, db: Session = Depends(get_db)):
    repo = UserRepository(db)

    # Check if the entity exists
    if not repo.user_exists(entity_id):
        raise HTTPException(status_code=404, detail="User not found")

    # Call the update method
    user = repo.get_user_by_id(entity_id)

    try:
        # Call the setter method to update the material
        repo.delete_user(user)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


    return {'message': "User deleted successfully"}

@app.put("/update_user/{entity_id}")
async def update_user(entity_id: int, request: UserUpdateRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    # Check if the entity exists
    if not repo.user_exists(entity_id):
        raise HTTPException(status_code=404, detail="User not found")

    # Call the update method
    user = repo.get_user_by_id(entity_id)
    try:
        # Call the setter method to update the user
        repo.update_user(user,
                             username=request.username,
                             email=request.email,
                             user_type_id=request.user_type_id,
                             password=request.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "User updated successfully"}

@app.post("/create_mattype")
async def create_material_type(request: MaterialTypeCreateRequest, db: Session = Depends(get_db)):
    repo = MaterialTypeRepository(db)

    type = db.query(MaterialType).filter_by(type_name=request.type_name).first()

    # Check if the entity exists
    if type is not None and repo.type_exists(type.id):
        raise HTTPException(status_code=404, detail="Material Type already exists")

    # Call the create method

    try:
        # Call the setter method to update the type
        repo.create_material_type(
                             type_name=request.type_name
                             )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material Type successfully created"}




@app.delete("/delete_mattype/{entity_id}")
async def delete_material_type(entity_id: int, db: Session = Depends(get_db)):
    repo = MaterialTypeRepository(db)

    # Check if the entity exists
    if not repo.type_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material Type not found")

    # Call the update method
    type = repo.get_material_type_by_id(entity_id)

    try:
        # Call the setter method to update the type
        repo.delete_material_type(type)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


    return {'message': "Material Type deleted successfully"}

@app.put("/update_mattype/{entity_id}")
async def update_material_type(entity_id: int, request: MaterialTypeUpdateRequest, db: Session = Depends(get_db)):
    repo = MaterialTypeRepository(db)
    # Check if the entity exists
    if not repo.type_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material Type not found")

    # Call the update method
    type = repo.get_material_type_by_id(entity_id)
    try:
        # Call the setter method to update the user
        repo.update_material_type(type,
                           type_name=request.type_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': "Material Type updated successfully"}

def get_app():
    return app