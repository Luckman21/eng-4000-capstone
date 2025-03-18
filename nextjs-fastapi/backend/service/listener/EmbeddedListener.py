from backend.controller import constants
from backend.controller import listener
from backend.controller.data_receiver import MQTTReceiver
from backend.controller.scale_listener import MQTTscale
import asyncio
from sqlalchemy import event
from db.model.Shelf import Shelf

# Define the MQTT receiver start function
def start_mqtt_receiver():
    mqtt_broker = "test.mosquitto.org"
    mqtt_port = 1883
    mqtt_temp_topic = "temp_value"
    mqtt_humid_topic = "humid_value"
    db_url = constants.DATABASE_URL

    receiver = MQTTReceiver(mqtt_broker, mqtt_port, mqtt_temp_topic, mqtt_humid_topic, db_url)
    receiver.start()

#Create a listener that triggers when the Material table is updated, checks for Materials with a mass below the threshold
# Define the MQTT scale start function
def start_mqtt_scale():
    mqtt_broker = "test.mosquitto.org"
    mqtt_port = 1883
    mqtt_topic = "mass_value"

    receiver = MQTTscale(mqtt_broker, mqtt_port, mqtt_topic)
    receiver.start()

    # Now the listener is running, and you can retrieve the latest value when needed.
    print(f"Latest value: {receiver.get_latest_value()}")


def shelf_listener():

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
