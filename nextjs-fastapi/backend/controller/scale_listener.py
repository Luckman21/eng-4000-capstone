import paho.mqtt.client as mqtt

class MQTTscale:
    def __init__(self, mqtt_broker, mqtt_port, mqtt_topic):
        # MQTT parameters
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.mqtt_topic = mqtt_topic
        
        # Store the latest value received
        self.latest_value = None

        # Initialize MQTT client
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
        """Process the received MQTT message."""
        try:
            # Store the latest received value (assuming the payload can be converted to float)
            self.latest_value = float(payload)
            print(f"Stored value: {self.latest_value}")
        except ValueError:
            print(f"Error: Failed to convert message payload to float: {payload}")

    def get_latest_value(self):
        """Return the latest value received."""
        return self.latest_value

    def start(self):
        """Start the MQTT client and begin receiving messages."""
        self.client.connect(self.mqtt_broker, self.mqtt_port, 60)
        self.client.loop_start()  # Starts the loop to receive messages in the background
