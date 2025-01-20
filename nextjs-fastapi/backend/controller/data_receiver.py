import paho.mqtt.client as mqtt
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from db.model import Shelf
from backend.controller import constants

class MQTTReceiver:
    def __init__(self, mqtt_broker, mqtt_port, mqtt_topic, db_url):
        # MQTT parameters
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic
        
        # Set up the SQLAlchemy session
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # MQTT client setup
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker."""
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(self.mqtt_topic)

    def on_message(self, client, userdata, msg):
        """Callback when a message is received."""
        print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
        self.process_message(msg.payload.decode())

    def process_message(self, payload):
        """Process the received MQTT message and update the shelf in the database."""
        try:
            # Assuming the payload is JSON formatted
            data = json.loads(payload)
            shelf_id = data.get('shelf_id')
            temperature = data.get('temperature')
            humidity = data.get('humidity')

            # Ensure all required fields are in the message
            if shelf_id and temperature is not None and humidity is not None:
                # Fetch the shelf by its ID
                shelf = self.session.query(Shelf).filter_by(id=shelf_id).first()
                
                if shelf:
                    # Update the shelf's temperature and humidity
                    shelf.temperature_cel = temperature
                    shelf.humidity_pct = humidity
                    self.session.commit()
                    print(f"Shelf {shelf_id} updated with temperature: {temperature}, humidity: {humidity}")
                else:
                    print(f"Shelf with ID {shelf_id} not found.")
            else:
                print("Invalid message format received. Missing shelf_id, temperature, or humidity.")
        except Exception as e:
            print(f"Error processing message: {e}")

    def start(self):
        """Start the MQTT client loop to receive messages."""
        self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        self.client.loop_start()

    def stop(self):
        """Stop the MQTT client loop."""
        self.client.loop_stop()

'''
# Usage Example:
if __name__ == "__main__":
    # Configure your MQTT broker and SQLAlchemy database URL
    mqtt_broker = "test.mqtt.org"
    mqtt_port = 1883
    mqtt_topic = "temp_value"
    db_url = constants.DATABASE_URL

    receiver = MQTTReceiver(mqtt_broker, mqtt_port, mqtt_topic, db_url)
    receiver.start()

    try:
        # Keep the program running to listen for messages
        while True:
            pass
    except KeyboardInterrupt:
        receiver.stop()
        print("Program stopped.")
'''