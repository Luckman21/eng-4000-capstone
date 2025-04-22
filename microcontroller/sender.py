import paho.mqtt.publish as publish

publish.single(
    topic="humid_value",
    payload="3|21.7",
    hostname="localhost",
    port=1883
)