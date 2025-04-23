from backend.controller import constants
from backend.service.listener import listener
from backend.service.listener.data_receiver import MQTTReceiver
from backend.service.listener.scale_listener import MQTTscale
from backend.service.listener.manager import manager
import asyncio
from sqlalchemy import event
from db.model.Shelf import Shelf

dht11_mqtt_instance = None
scale_mqtt_instance = None

# Define the MQTT receiver start function
def start_mqtt_receiver():
    global dht11_mqtt_instance
    dht11_mqtt_instance = MQTTReceiver(
        mqtt_broker="test.mosquitto.org",
        mqtt_port=1883,
        mqtt_temp_topic="temp_value",
        mqtt_humid_topic="humid_value",
        db_url=constants.DATABASE_URL
    )
    dht11_mqtt_instance.start()

#Create a listener that triggers when the Material table is updated, checks for Materials with a mass below the threshold
# Define the MQTT scale start function
def start_mqtt_scale():
    global scale_mqtt_instance
    scale_mqtt_instance = MQTTscale(
        mqtt_broker="test.mosquitto.org",
        mqtt_port=1883,
        mqtt_topic="mass_value"
    )

    # Now the listener is running, and you can retrieve the latest value when needed.
    print(f"Latest value: {scale_mqtt_instance.get_latest_value()}")
    scale_mqtt_instance.start()

def shelf_listener(LOOP):

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

def get_scale_listener():

    return scale_mqtt_instance