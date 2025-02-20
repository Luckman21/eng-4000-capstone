import json
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
from db.repositories.UserTypeRepository import UserTypeRepository
import asyncio
from fastapi import  WebSocket, WebSocketDisconnect
from sqlalchemy import event
from backend.controller import constants
from backend.controller import listener
from backend.controller.schemas.MaterialUpdateRequest import MaterialUpdateRequest
from backend.controller.schemas.MaterialCreateRequest import MaterialCreateRequest
from db.repositories.MaterialTypeRepository import MaterialTypeRepository
from backend.controller.schemas.UserUpdateRequest import UserUpdateRequest
from backend.controller.schemas.UserCreateRequest import UserCreateRequest
from backend.controller.schemas.MaterialTypeUpdateRequest import MaterialTypeUpdateRequest
from backend.controller.schemas.MaterialTypeCreateRequest import MaterialTypeCreateRequest
from backend.controller.schemas.MaterialMutationRequest import MaterialMutationRequest
from backend.controller.data_receiver import MQTTReceiver
from backend.service.PasswordHashService import PasswordHashService
from fastapi import FastAPI, Depends, HTTPException, Response,Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional
from backend.service.mailer.TempPasswordMailer import TempPasswordMailer
from backend.service.mailer.PasswordChangeMailer import PasswordChangeMailer
from backend.service.TempPasswordRandomizeService import create_temp_password
from backend.controller.schemas.ForgotPasswordRequest import ForgotPasswordRequest
from backend.service.PasswordHashService import PasswordHashService



app = FastAPI()
origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,  # Allow frontend origin
    allow_credentials=True,  # REQUIRED to allow cookies
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


############################################################################################################ Testing login stuff
# Configurations

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
hash = PasswordHashService()
# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create JWT access token
    access_token = create_access_token(
        data={"username": user.username, "user_type_id": user.user_type_id, "email": user.email, "id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Prevent JavaScript access (XSS protection)
        secure=False,  # Requires HTTPS in production
        samesite="Lax",  # Prevents CSRF but allows login flow
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Set expiration
        path="/",  # Apply to all routes
    )

    return {"message": "Login successful"}

def authenticate_user(username: str, password: str, db: Session):
    repo = UserRepository(db)
    user = repo.get_user_by_username(username)

    if hash.check_password(username, password, db):
        return user
    else:
        return None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, constants.SECRET_KEY, algorithm=ALGORITHM)


@app.post("/logout")
def logout(response: Response):
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=False,  # Secure=True only in production
        samesite="Lax",
        max_age=0,  # Expire immediately
        path="/",
    )
    return {"message": "Logged out successfully"}




@app.get("/protected")
def protected_route(request: Request, response: Response):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_access_token(token)
        # Generate a new token with an updated expiration time
        new_token = create_access_token(
            data={"username": payload["username"], "user_type_id": payload["user_type_id"]},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),  # Reset expiration
        )

        # Update the cookie with the new token
        response.set_cookie(
            key="access_token",
            value=new_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
        )

        return {"message": "Access granted", "user": payload}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, constants.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


############################################################################################################


# Set up listeners on startup
@app.on_event("startup")
def setup_listeners():
    low_stock_listener()

# Set up listeners on startup
@app.on_event("startup")
def setup_mqtt():
    start_mqtt_receiver()

# Define the MQTT receiver start function
def start_mqtt_receiver():
    mqtt_broker = "test.mosquitto.org"
    mqtt_port = 1883
    mqtt_temp_topic = "temp_value"
    mqtt_humid_topic = "humid_value"
    db_url = constants.DATABASE_URL

    receiver = MQTTReceiver(mqtt_broker, mqtt_port, mqtt_temp_topic, mqtt_humid_topic, db_url)
    receiver.start()






# Store active WebSocket connections
active_connections = []

# Create a listener that triggers when the Material table is updated, checks for Materials with a mass below the threshold
def low_stock_listener():
    def listener_wrapper(mapper, connection, target):
        asyncio.create_task(listener.job_complete_listener(mapper, connection, target))

    event.listen(Material, 'after_update', listener_wrapper)

@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connections for real-time material alerts."""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            print("Waiting for alert...")
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)




# Now define your API routes
@app.get("/materials", response_model=list[MaterialSchema])
async def get_Allmaterials(db: Session = Depends(get_db)):
    repo = MaterialRepository(db)
    return repo.get_all_materials()

@app.get("/material_types")
async def get_all_material_types(db: Session = Depends(get_db)):
    repo =MaterialTypeRepository(db)
    return repo.get_all_material_types()

@app.get("/user_types")
async def get_all_user_types(db: Session = Depends(get_db)):
    repo =UserTypeRepository(db)
    return repo.get_all_user_types()

@app.get("/users")
async def get_all_users(db: Session = Depends(get_db)):
    repo =UserRepository(db)
    return repo.get_all_users()

@app.post("/create_material")
async def create_material(request: MaterialCreateRequest, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)

    material = db.query(Material).filter_by(supplier_link=request.supplier_link, colour=request.colour, material_type_id=request.material_type_id).first()

    # Check if the entity exists
    if material is not None and repo.material_exists(material.id):
        raise HTTPException(status_code=404, detail="Material already exists")

    # Call the update method

    try:
        # Call the setter method to update the material
        repo.create_material(
                             colour=request.colour,
                             supplier_link=request.supplier_link,
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
                             supplier_link=request.supplier_link,
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
                             password=PasswordHashService.hash_password(request.password),
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
        password = None
        if request.password is not None:
            password = PasswordHashService.hash_password(request.password)

        repo.update_user(user,
                             username=request.username,
                             password= password,
                             email=request.email,
                             user_type_id=request.user_type_id
                             )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        if request.password is not None:
            mailer = PasswordChangeMailer(from_addr=constants.MAILER_EMAIL)
            mailer.send_notification(user.email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    new_token = create_access_token(data={
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "user_type_id": user.user_type_id,
    })

    return {'message': "User updated successfully", "access_token": new_token}

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

@app.post("/forgot_password/")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):

    repo = UserRepository(db)
    # Check if the entity exists
    if not repo.user_email_exists(request.email):
        raise HTTPException(status_code=404, detail="User not found")

    user = repo.get_user_by_email(request.email)

    # Create password, update, and send

    plain_password = create_temp_password()
    hashed_password = PasswordHashService.hash_password(plain_password)

    try:
        # Call the setter method to update the user

        repo.update_user(user,
                           password=hashed_password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        mailer = TempPasswordMailer(from_addr=constants.MAILER_EMAIL)
        mailer.send_notification(user.email, plain_password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {'message': "Password successfully sent"}


@app.patch("/replenish_mass/{entity_id}")
def replenish_mass(entity_id: int, request: MaterialMutationRequest, db: Session = Depends(get_db) ):
    repo = MaterialRepository(db)
    # Check if the entity exists

    if not repo.material_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material not found")

    # Call the update method
    material = repo.get_material_by_id(entity_id)
    try:
        # Call the setter method to update the material
        repo.update_material(material,
                             mass=(material.mass + request.mass_change),
                             colour=None,
                             material_type_id=None,
                             supplier_link=None,
                             shelf_id=None)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': f"{request.mass_change} grams replenished"}


@app.patch("/consume_mass/{entity_id}")
def consume_mass(entity_id: int, request: MaterialMutationRequest, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)
    # Check if the entity exists
    if not repo.material_exists(entity_id):
        raise HTTPException(status_code=404, detail="Material not found")

    # Call the update method
    material = repo.get_material_by_id(entity_id)

    #Check mass diference

    if request.mass_change > material.mass:
        raise HTTPException(status_code=400, detail="Consumed mass greater than material's mass")
    try:
        # Call the setter method to update the material
        repo.update_material(material,
                             mass=(material.mass - request.mass_change),
                             colour=None,
                             material_type_id=None,
                             supplier_link=None,
                             shelf_id=None)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'message': f"{request.mass_change} grams consumed"}


def get_app():

    return app