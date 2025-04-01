import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    """Manages active WebSocket connections."""
    def __init__(self):
        self.active_connections = set()
        print(f"Connection Manager initialized with id {id(self)}")

    async def connect(self, websocket: WebSocket):
        """Accept WebSocket connection and store it."""
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"WebSocket connected: {websocket.client} - Total connections: {len(self.active_connections)}")

    async def disconnect(self, websocket: WebSocket):
        """Remove disconnected WebSocket."""
        self.active_connections.remove(websocket)
        print(f"WebSocket disconnected: {websocket.client} - Total connections: {len(self.active_connections)}")

    async def send_alerts(self, alert_materials):
        """Send alerts to all connected clients."""
        if not self.active_connections:
            print("⚠️ No active WebSockets to send alerts to!")
            return

        print(f"Sending alerts to {len(self.active_connections)} clients...")

        for ws in self.active_connections.copy():
            try:
                await ws.send_text(alert_materials)
                print(f"📤 Sent alert to client {ws.client}")
            except Exception as e:
                print(f"⚠️ Error sending message to {ws.client}: {e}")
                self.active_connections.remove(ws)  # Remove disconnected clients

# Create manager instance
manager = ConnectionManager()
