import sys
from pathlib import Path

import uvicorn
sys.path.append(str(Path().resolve().parent.parent))
from sqlalchemy.orm import Session
from backend.controller.dependencies import get_db
from db.model.Material import Material
from db.model.Shelf import Shelf
from db.model.User import User
from db.model.MaterialType import MaterialType
from db.model.UserType import UserType
from fastapi.middleware.cors import CORSMiddleware
from db.repositories.UserTypeRepository import UserTypeRepository
import asyncio
from sqlalchemy import event
from backend.controller import constants
from backend.controller import listener
from backend.controller.data_receiver import MQTTReceiver
from backend.controller.scale_listener import MQTTscale
from fastapi import FastAPI, Depends, HTTPException, Response, Request
from backend.controller.routers import materials, material_types, users, access_management, qr
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import jwt
from fastapi import  WebSocket, WebSocketDisconnect
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional
from backend.service.mailer.TempPasswordMailer import TempPasswordMailer
from backend.service.mailer.PasswordChangeMailer import PasswordChangeMailer
from backend.service.TempPasswordRandomizeService import create_temp_password
from backend.controller.schemas.ForgotPasswordRequest import ForgotPasswordRequest
from backend.service.PasswordHashService import PasswordHashService
from backend.controller.manager import manager

app = FastAPI()
app.include_router(materials.router)
app.include_router(material_types.router)
app.include_router(users.router)
app.include_router(access_management.router)
app.include_router(qr.router)

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow frontend origin
    allow_credentials=True,  # REQUIRED to allow cookies
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
async def root():
    return {"message": "Hello Azure"}

LOOP = None

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Set up listeners on startup
@app.on_event("startup")
async def setup_listeners():
    global LOOP
    LOOP = asyncio.get_running_loop()
    low_stock_listener()
    shelf_listener()

#Set up listeners on startup

# Set up listeners on startup
@app.on_event("startup")
def setup_mqtt():
    start_mqtt_receiver()
    start_mqtt_scale()


# Define the MQTT receiver start function
def start_mqtt_receiver():
    mqtt_broker = "test.mosquitto.org"
    mqtt_port = 1883
    mqtt_temp_topic = "temp_value"
    mqtt_humid_topic = "humid_value"
    db_url = constants.DATABASE_URL

    receiver = MQTTReceiver(mqtt_broker, mqtt_port, mqtt_temp_topic, mqtt_humid_topic, db_url)
    receiver.start()

#Create a listener that triggers when the Material table is updated, checks for Materials with a mass below the threshold
# Define the MQTT scale start function
def start_mqtt_scale():
    mqtt_broker = "test.mosquitto.org"
    mqtt_port = 1883
    mqtt_topic = "mass_value"

    receiver = MQTTscale(mqtt_broker, mqtt_port, mqtt_topic)
    receiver.start()

    # Now the listener is running, and you can retrieve the latest value when needed.
    print(f"Latest value: {receiver.get_latest_value()}")

# Create a listener that triggers when the Material table is updated, checks for Materials with a mass below the threshold
def low_stock_listener():
    def listener_wrapper(mapper, connection, target):
        asyncio.create_task(listener.job_complete_listener(mapper, connection, target))
    event.listen(Material, 'after_update', listener_wrapper)

def shelf_listener():

    def shelf_update_listener(mapper, connection, target):
        print(f"🆔 Manager ID (shelf_listener): {id(manager)}")  # Ensure it's the same instance
        try:
            future = asyncio.run_coroutine_threadsafe(listener.shelf_update_listener(mapper, connection, target), LOOP)
            future.result()  # Ensure exceptions are caught
            print("✅ Successfully ran shelf listener")
        except RuntimeError as e:
            print(f"❌ RuntimeError: {e} - Possibly no running event loop?")
        except Exception as e:
            print(f"❌ Error in shelf_update_listener: {e}")
    event.listen(Shelf, 'after_update', shelf_update_listener)


@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connections for real-time alerts."""
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()  # Keep the connection alive
    except WebSocketDisconnect:
        await manager.disconnect(websocket)




# Now define your API routes
@app.get("/materials", response_model=list[MaterialSchema])
async def get_Allmaterials(db: Session = Depends(get_db)):
    repo = MaterialRepository(db)
    return repo.get_all_materials()


@app.get("/material_types")
async def get_all_material_types(db: Session = Depends(get_db)):
    repo = MaterialTypeRepository(db)
    return repo.get_all_material_types()


@app.get("/user_types")
async def get_all_user_types(db: Session = Depends(get_db)):
    repo = UserTypeRepository(db)
    return repo.get_all_user_types()

def get_app():
    return app
