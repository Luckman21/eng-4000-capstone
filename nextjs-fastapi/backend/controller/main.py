import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent.parent))
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.controller.dependencies import get_db
from db.schemas import MaterialSchema 
from db.model.Material import Material
from fastapi.middleware.cors import CORSMiddleware
from db.repositories.MaterialRepository import MaterialRepository
# from backend.controller.schemas import MassUpdateRequest, MassUpdateResponse
from pydantic import BaseModel
import asyncio
from sqlalchemy import event
from backend.controller import listener
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

class MassUpdateRequest(BaseModel):
    mass: float

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

# Track active WebSocket connections
active_connections = []

# WebSocket connection manager
class WebSocketManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, user_id: str, message: dict):
        """
        Send a message to a specific WebSocket connection identified by user_id.
        """
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)
            print(f"Sent message to {user_id}.")
        else:
            print(f"User {user_id} not connected.")

    async def send_to_all(self, data: dict):
        # Send data to all active WebSocket clients
        for connection in self.active_connections:
            await connection.send_json(data)

# Create the WebSocket manager instance
ws_manager = WebSocketManager()

# Set up listeners on startup
@app.on_event("startup")
def setup_listeners():
    low_stock_listener()

# Create a listener that triggers when the Material table is updated, checks for Materials with a mass below the threshold
def low_stock_listener():
    def listener_wrapper(mapper, connection, target):
        asyncio.create_task(listener.job_complete_listener(mapper, connection, target))

    event.listen(Material, 'after_update', listener_wrapper)

# WebSocket connection handler
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket endpoint where each user is identified by user_id.
    """
    print(f"WebSocket connection attempt for {user_id}...")
    await ws_manager.connect(websocket, user_id)
    print(f"WebSocket connection established for {user_id}.")

    try:
        while True:
            # Keep the connection alive by receiving text (you can modify as needed)
            await websocket.receive_text()
    except WebSocketDisconnect:
        print(f"Websocket {user_id} disconnected.")
        ws_manager.disconnect(user_id)

# Now define your API routes
@app.get("/materials", response_model=list[MaterialSchema])
async def get_Allmaterials(db: Session = Depends(get_db)):
    repo = MaterialRepository(db)
    return repo.get_all_materials()

# @app.get("/materials/{material_type}")

@app.put("/update_mass/{entity_id}")
async def update_mass(entity_id: int, request: MassUpdateRequest, db: Session = Depends(get_db)):
    repo = MaterialRepository(db)

    # Check if the entity exists
    if not repo.material_exists(entity_id):
        raise HTTPException(status_code=404, detail="Mass entity not found")

    # Call the update method
    material = repo.get_material_by_id(entity_id)

    try:
        # Call the setter method to update the mass
        repo.update_material(material, mass=request.mass)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    material = repo.get_material_by_id(entity_id)

    return {'message': "Mass updated successfully", 'new_mass' : material.mass}

def get_app():
    return app