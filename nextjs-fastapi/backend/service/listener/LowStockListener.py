import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent.parent))
import asyncio
from sqlalchemy import event
from db.model.Material import Material
from backend.controller import listener


def low_stock_listener():
    def listener_wrapper(mapper, connection, target):
        asyncio.create_task(listener.job_complete_listener(mapper, connection, target))
    event.listen(Material, 'after_update', listener_wrapper)
