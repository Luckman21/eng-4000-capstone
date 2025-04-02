import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    """Manages active WebSocket connections with buffering."""
    _instance = None  # Private instance

    def __new__(cls):
        """Override the default instance creation to ensure singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.active_connections = set()
            cls._instance.alert_queue = asyncio.Queue()
            print(f"Connection Manager instance created at {id(cls._instance)}")
        return cls._instance

    async def connect(self, websocket: WebSocket):
        """Accept WebSocket connection and store it."""
        await websocket.accept()
        self.active_connections.add(websocket)

    async def disconnect(self, websocket: WebSocket):
        """Remove disconnected WebSocket."""
        self.active_connections.remove(websocket)

    async def send_alerts(self, alert_materials):
        """Push alert to queue for processing and sending."""
        await self.alert_queue.put(alert_materials)
        print("📝 Alert queued for processing")

    async def process_alerts(self):
        """Process and send alerts to all connected clients."""
        while True:
            print("⏳ Waiting for alert in queue...")
            # Wait for an alert to be put in the queue
            alert_materials = await self.alert_queue.get()
            print("📤 Processing alert from queue")

            if not self.active_connections:
                print("⚠️ No active WebSockets to send alerts to!")
                continue

            for ws in self.active_connections.copy():
                try:
                    await ws.send_text(alert_materials)
                    print("📤 Sent alert to client")
                except Exception as e:
                    print(f"⚠️ Error sending message: {e}")
                    self.active_connections.remove(ws)  # Remove disconnected clients

# create manager instance
manager = ConnectionManager()

# Run the background task that processes alerts
async def start_alert_processor():
    await manager.process_alerts()

# In your FastAPI app, start the background task like this:
# app.add_event_handler("startup", start_alert_processor())
