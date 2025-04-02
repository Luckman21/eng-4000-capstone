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
        """Continuously process the command queue, batching alerts to prevent flooding."""
        while True:
            try:
                if self.command_queue.empty():
                    await asyncio.sleep(0.5)  # Reduce CPU usage
                    continue

                batch_alerts = []
                while not self.command_queue.empty():
                    batch_alerts.append(await self.command_queue.get())
                    self.command_queue.task_done()

                if batch_alerts:
                    alert_message = json.dumps({"batch": batch_alerts})
                    await self.send_alerts(alert_message)
                    await asyncio.sleep(0.2)  # Prevent message storms

            except Exception as e:
                print(f"❌ Error processing command queue: {e}")

    async def send_alerts(self, alert_materials):
        """Send alerts to all connected clients with improved error handling."""
        if not self.active_connections:
            print("⚠️ No active WebSockets to send alerts to!")
            return

        print(f"📢 Sending alert to {len(self.active_connections)} clients...")

        disconnected_clients = set()
        for ws in self.active_connections.copy():
            try:
                await ws.send_text(alert_materials)
                print(f"✅ Alert sent to {ws.client}")
                await asyncio.sleep(0.1)  # Prevent flooding
            except WebSocketDisconnect:
                print(f"❌ Client {ws.client} disconnected.")
                disconnected_clients.add(ws)
            except Exception as e:
                print(f"⚠️ Error sending message to {ws.client}: {e}")
                disconnected_clients.add(ws)

        # Remove disconnected clients
        self.active_connections -= disconnected_clients


# Create manager instance
manager = ConnectionManager()
print("manager ready")


# To start processing the command queue
async def start_processing_commands():
    await manager.process_command_queue()
