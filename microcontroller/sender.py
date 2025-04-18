import paho.mqtt.publish as publish

publish.single(
    topic="humid_value",
    payload="1|23.2",
    hostname="test.mosquitto.org",
    port=1883
)