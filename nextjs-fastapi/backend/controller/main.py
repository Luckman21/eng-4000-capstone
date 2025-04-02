import sys
from pathlib import Path

import uvicorn

sys.path.append(str(Path().resolve().parent.parent))
from sqlalchemy.orm import Session
from backend.controller.dependencies import get_db
from fastapi.middleware.cors import CORSMiddleware
from db.repositories.UserTypeRepository import UserTypeRepository
import asyncio
from fastapi import FastAPI, Depends
from backend.controller.routers import materials, material_types, users, access_management, qr
from fastapi import WebSocket, WebSocketDisconnect
from backend.service.listener.manager import manager, start_alert_processor
from backend.service.listener.LowStockListener import low_stock_listener
from backend.service.listener import EmbeddedListener

app = FastAPI()
app.include_router(materials.router)
app.include_router(material_types.router)
app.include_router(users.router)
app.include_router(access_management.router)
app.include_router(qr.router)

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://eng-4000-capstone-delta.vercel.app",
    "https://capstone-teal.vercel.app/"
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
mqtt_service = {"dht_connection": True, "scale_connection" : True}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Set up listeners on startup
@app.on_event("startup")
async def setup_listeners():
    global LOOP
    LOOP = asyncio.get_running_loop()
    low_stock_listener()
    EmbeddedListener.shelf_listener(LOOP)
    asyncio.create_task(start_alert_processor())


# Set up listeners on startup
@app.on_event("startup")
def setup_mqtt():
    "Establish an MQTT connection. Report MQTT service outages"
    global mqtt_service
    try:
        EmbeddedListener.start_mqtt_receiver()
        mqtt_service["dht_connection"] = True
    except Exception:
        print("Failed to connect to DHT-11")
        mqtt_service["dht_connection"] = False
    try:
        EmbeddedListener.start_mqtt_scale()
        mqtt_service["scale_connection"] = True
    except Exception:
        print("Failed to connect to scale")
        mqtt_service["scale_connection"] = False

@app.get("/mqtt-status")
def get_mqtt_status():

    "Return the status of the MQTT services"
    return mqtt_service

@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connections for real-time alerts."""
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()  # Keep the connection alive
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


@app.get("/user_types")
async def get_all_user_types(db: Session = Depends(get_db)):
    repo = UserTypeRepository(db)
    return repo.get_all_user_types()


def get_app():
    return app
