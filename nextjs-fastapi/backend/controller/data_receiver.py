import paho.mqtt.client as mqtt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.repositories.ShelfRepository import ShelfRepository

class MQTTReceiver:
    def __init__(self, mqtt_broker, mqtt_port, mqtt_temp_topic, mqtt_humid_topic, db_url):
        # MQTT parameters
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_temp_topic = mqtt_temp_topic
        self.mqtt_humid_topic = mqtt_humid_topic
        
        # Set up the SQLAlchemy session
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Initialize ShelfRepository
        self.shelf_repository = ShelfRepository(self.session)  # Proper initialization

        # MQTT client setup
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # Store the temperature and humidity values to process later
        self.temperature = None
        self.humidity = None

    def on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker."""
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(self.mqtt_temp_topic)
        client.subscribe(self.mqtt_humid_topic)

    def on_message(self, client, userdata, msg):
        """Callback when a message is received."""
        print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
        self.process_message(msg.topic, msg.payload.decode())

    def process_message(self, topic, payload):
        """Process the received MQTT message."""

        shelf_id = payload[:payload.find("|")]
        data = payload[payload.find("|") + 1:]
        try:
            if topic == self.mqtt_temp_topic:
                # Received temperature data
                self.temperature = float(data)
                print(f"Received temperature: {self.temperature}")
                self.update_shelf(shelf_id, None, self.temperature)
            elif topic == self.mqtt_humid_topic:
                # Received humidity data
                self.humidity = float(data)
                print(f"Received humidity: {self.humidity}")

            # If both temperature and humidity are received, update the database
            if self.temperature is not None and self.humidity is not None:
                # You would need to send the correct shelf_id based on your system logic
                shelf_id = 1  # Example: Update shelf with ID 1
                self.update_shelf(shelf_id, self.humidity, self.temperature)
                # Reset the values to wait for new data
                self.temperature = None
                self.humidity = None
                self.update_shelf(shelf_id, self.humidity, None)

        except Exception as e:
            print(f"Error processing message: {e}")

    def update_shelf(self, shelf_id, temperature, humidity):
        """Update the Shelf object in the database."""
        try:
            # Use ShelfRepository to fetch the shelf
            shelf = self.shelf_repository.get_shelf_by_id(shelf_id)  # Use the instance here

            if shelf:
                # Use ShelfRepository to update the shelf
                self.shelf_repository.update_shelf(shelf, humidity, temperature)
                print(f"Shelf {shelf_id} updated with temperature: {temperature}, humidity: {humidity}")
            else:
                print(f"Shelf with ID {shelf_id} not found.")
        except Exception as e:
            print(f"Error updating shelf: {e}")

        # Debug Print Statements
        #print(f"shelf temp: {self.shelf_repository.get_shelf_by_id(shelf_id).temperature_cel}")
        #print(f"shelf humid: {self.shelf_repository.get_shelf_by_id(shelf_id).humidity_pct}")

    def start(self):
        """Start the MQTT client loop to receive messages."""
        self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        self.client.loop_start()

    def stop(self):
        """Stop the MQTT client loop."""
        self.client.loop_stop()

    def get_temp(self):
        """Returns the last stored value for the temperature."""
        return self.temperature

    def get_humid(self):
        """Returns the last stored value for the humidity."""
        return self.humidity
