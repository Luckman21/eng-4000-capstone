import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from asyncio import Queue
import logging


class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self):
        self.active_connections = set()
        self.command_queue = Queue()  # Queue for commands/alerts
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

    async def queue_alert(self, alert_materials):
        """Adds an alert to the command queue."""
        await self.command_queue.put(alert_materials)
        print(f"Alert queued: {alert_materials}")

    async def process_command_queue(self):
        """Process the command queue and send alerts at a controlled rate."""
        while True:
            if not self.command_queue.empty():
                alert_materials = await self.command_queue.get()
                await self.send_alerts(alert_materials)
                self.command_queue.task_done()
            else:
                await asyncio.sleep(0.1)  # Brief sleep if no commands to process

    async def send_alerts(self, alert_materials):
        """Send alerts to all connected clients."""
        if not self.active_connections:
            print("⚠️ No active WebSockets to send alerts to!")
            return

        print(f"Sending alert to {len(self.active_connections)} clients...")

        # Send alert to all active WebSockets
        for ws in self.active_connections.copy():
            try:
                await ws.send_text(alert_materials)
                print(f"📤 Sent alert to client {ws.client}")
            except Exception as e:
                print(f"⚠️ Error sending message to {ws.client}: {e}")
                self.active_connections.remove(ws)  # Remove disconnected clients


# Create manager instance
manager = ConnectionManager()


# To start processing the command queue
async def start_processing_commands():
    await manager.process_command_queue()
