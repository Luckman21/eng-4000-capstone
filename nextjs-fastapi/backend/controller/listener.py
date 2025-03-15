import asyncio
import json
from db.repositories.MaterialRepository import MaterialRepository
from db.repositories.ShelfRepository import ShelfRepository
from backend.controller import constants
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from backend.controller.manager import manager
from asyncio import get_running_loop
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from backend.service.mailer.LowStockMailer import LowStockMailer
from backend.service.mailer.EnviroWarningMailer import EnviroWarningMailer
from db.repositories.UserRepository import UserRepository
from backend.controller.ApplicationState import app_state

DATABASE_URL = constants.DATABASE_URL_ASYNC  # Example: "postgresql+asyncpg://user:password@localhost/dbname"

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create an async session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

async def quantity_poll(materials):
    alerts = []
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)
        superadmins = await user_repo.get_all_superadmins_async()


    for material in materials:
        if material.mass < constants.THRESHOLD:
            alerts.append(material)

    for alert in alerts:
        previous_mass = app_state.get_previous_material_state(alert.id)

        if previous_mass is not None and previous_mass >= constants.THRESHOLD:
            for superadmin in superadmins:
                LowStockMailer(constants.MAILER_EMAIL).send_notification(superadmin.email, alert.material_type.type_name, alert.colour, alert.supplier_link)

    return alerts

async def job_complete_listener(mapper, connection, target):
    session = AsyncSessionLocal()
    print(f"🆔 Manager ID (listener): {id(manager)}")

    # Create MaterialRepository instance
    repo = MaterialRepository(session)
    materials = await repo.get_all_materials_async()

    alert_materials = await quantity_poll(materials)

    session.close()

    # Track previous states
    for material in materials:
        app_state.set_previous_material_state(material.id, material.mass)

    data = {
        "type": "material_alert",
        "data": [
            {"id": m.id, "colour": m.colour, "mass": m.mass, "supplier_link": m.supplier_link} for m in alert_materials
        ] if alert_materials else []
    }

    json_data = json.dumps(data)
    if json_data:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(manager.send_alerts(json_data))
        else:
            asyncio.run(manager.send_alerts(json_data))

    return alert_materials


async def shelf_update_listener(mapper, connection, target):
    try:
        async with AsyncSessionLocal() as session:
            repo = ShelfRepository(session)
            user_repo = UserRepository(session)
            superadmins = await user_repo.get_all_superadmins_async()
            high_humidity_shelves = await repo.get_high_humidity_shelves_async()
            high_temp_shelves = await repo.get_high_temperature_shelves_async()

            alert_shelfs = []

            for shelf in high_humidity_shelves + high_temp_shelves:
                # Check if shelf state has changed (from acceptable to unacceptable)
                previous_state = app_state.get_previous_shelf_state(shelf.id)
                if previous_state is None:
                    app_state.set_previous_shelf_state(shelf.id, shelf.humidity_pct, shelf.temperature_cel)
                else:
                    # Check if the humidity or temperature crossed the threshold
                    if shelf.humidity_pct > constants.HUMIDITY_TOLERANCE >= previous_state['humidity']:
                        for superadmin in superadmins:
                            EnviroWarningMailer(constants.MAILER_EMAIL).send_notification(superadmin.email, "humidity", shelf.id)
                    if shelf.temperature_cel > constants.TEMPERATURE_TOLERANCE >= previous_state['temperature']:
                        for superadmin in superadmins:
                            EnviroWarningMailer(constants.MAILER_EMAIL).send_notification(superadmin.email, "temperature", shelf.id)

                # Update the previous states
                app_state.set_previous_shelf_state(shelf.id, shelf.humidity_pct, shelf.temperature_cel)

                # Keep the shelves that need alert
                alert_shelfs.append(shelf)

    except Exception as e:
        print(f"Error while fetching shelves: {e}")
        return []

    if alert_shelfs:
        data = {
            "type": "shelf_alert",
            "data": [
                {"id": s.id, "humidity": s.humidity_pct, "temperature": s.temperature_cel}
                for s in alert_shelfs
            ]
        }

        json_data = json.dumps(data)

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(manager.send_alerts(json_data))
            else:
                asyncio.run_coroutine_threadsafe(manager.send_alerts(json_data), loop)
        except Exception as e:
            print(f"❌ Error while scheduling alert: {e}")

