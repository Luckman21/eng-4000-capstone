import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    """Manages active WebSocket connections."""
    def __init__(self):
        self.active_connections = set()

    async def connect(self, websocket: WebSocket):
        """Accept WebSocket connection and store it."""
        await websocket.accept()
        self.active_connections.add(websocket)

    async def disconnect(self, websocket: WebSocket):
        """Remove disconnected WebSocket."""
        self.active_connections.remove(websocket)

    async def send_alerts(self, alert_materials):
        """Send alerts to all connected clients."""

        if not self.active_connections:
            print("⚠️ No active WebSockets to send alerts to!")
            return

        for ws in self.active_connections.copy():
            try:
                await ws.send_text(alert_materials)
            except Exception as e:
                print(f"⚠️ Error sending message: {e}")
                self.active_connections.remove(ws)  # Remove disconnected clients

# create manager instance 
manager = ConnectionManager()
