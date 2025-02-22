#define YORKU_SSID "" // move to cred.h
#define YORKU_PASS "" // move to cred.h
#define DHTPIN 7
#define DHTTYPE 11
#define TEMP_CAL 21 // Adjusts the temperature reading for accuracy
#define HUMID_CAL 15  // Adjusts the humidity reading for accuracy

//#include "cred.h" // wifi credentials
#include <ArduinoMqttClient.h>
#include <WiFiNINA.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

int temp_sensor_inPin = 7;

char ssid[] = YORKU_SSID; // network SSID (name)
char pass[] = YORKU_PASS; // network password (used for WPA, or as a key for WEP)

WiFiClient wiFiClient;              // Create a wifiClient
MqttClient mqttClient(wiFiClient);  // Connect wifiClient to MqttClient

DHT_Unified dht(DHTPIN, DHTTYPE); // Specify pin and sensor model

const char broker[] = "test.mosquitto.org";
int port = 1883;
const char topic_temp[] = "temp_value";
const char topic_humid[] = "humid_value";

// Create an interval for sending messages (in milliseconds)
const long interval = 8000;
unsigned long prev_ms = 0;

void setup() {
  Serial.begin(9600);

  // set up DHT sensor
  dht.begin();
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);

  // attempt to connect to Wifi network
  Serial.print("Attempting to connect to WPA SSID: ");
  Serial.println(ssid);
  while(WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }

  Serial.println("Connected to network.\n");
  Serial.println("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed\nError Code = ");
    Serial.println(mqttClient.connectError());  // Prints the error code for debugging
    while (1);  // Keep trying until connection is successful
  }

  Serial.println("Connected to MQTT broker.\n");
}

void loop() {
  mqttClient.poll();  // Sends MQTT keep alive, constantly called to keep connection alive

  unsigned long curr_ms = millis();

  if (curr_ms - prev_ms >= interval) {
    prev_ms = curr_ms;

    sensors_event_t temp_event;
    dht.temperature().getEvent(&temp_event);

    sensors_event_t humid_event;
    dht.humidity().getEvent(&humid_event);

    float temp = temp_event.temperature;
    float humid = humid_event.relative_humidity;

    // Log updates to serial monitor
    Serial.print("Send temp to topic_temp: ");
    Serial.println(topic_temp);
    Serial.println(temp + TEMP_CAL);

    Serial.print("Send humid to topic_humid: ");
    Serial.println(topic_humid);
    Serial.println(humid + HUMID_CAL);

    // Send message, using print to send message contents
    mqttClient.beginMessage(topic_temp);
    mqttClient.print(temp + TEMP_CAL);
    mqttClient.endMessage();

    mqttClient.beginMessage(topic_humid);
    mqttClient.print(humid + HUMID_CAL);
    mqttClient.endMessage();

    Serial.println();
  }
}