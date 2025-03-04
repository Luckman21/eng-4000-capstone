//#include "cred.h" // wifi credentials
#include <ArduinoMqttClient.h>
#include <WiFiNINA.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include "HX711.h"

#define YORKU_SSID "" // move to cred.h
#define YORKU_PASS "" // move to cred.h
#define DHTPIN 7
#define DHTTYPE 11
#define TEMP_CAL 21 // Adjusts the temperature reading for accuracy
#define HUMID_CAL 15  // Adjusts the humidity reading for accuracy
// Define HX711 pins
#define DOUT 2   // Data pin (DT)
#define CLK 3    // Clock pin (SCK)
#define BUTTON_PIN 4  // Button pin to tare the scale
// Define display pins for 7SD
#define DT 8
#define SCLK 9

int temp_sensor_inPin = 7;

// Note: HX711 will require its own power source.  Make sure to connect all wires to a common ground to the Arduino
HX711 scale;  // Create HX711 object

char ssid[] = YORKU_SSID; // network SSID (name)
char pass[] = YORKU_PASS; // network password (used for WPA, or as a key for WEP)

WiFiClient wiFiClient;              // Create a wifiClient
MqttClient mqttClient(wiFiClient);  // Connect wifiClient to MqttClient

DHT_Unified dht(DHTPIN, DHTTYPE); // Specify pin and sensor model

const char broker[] = "test.mosquitto.org";
int port = 1883;
const char topic_temp[] = "temp_value";
const char topic_humid[] = "humid_value";
const char topic_mass[] = "mass_value";

// Create an interval for sending messages (in milliseconds)
const long interval = 8000;
unsigned long prev_ms = 0;

long prev_weight = 0; // Stores the value of the previous recorded weight, used to compare with the current reading

void setup() {
  Serial.begin(57600);

  // set up DHT sensor
  dht.begin();
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);

  delay(1000);  // Allow some time for the HX711 to stabilize

  // Initialize HX711
  scale.begin(DOUT, CLK);

  // Check if HX711 is ready
  if (scale.is_ready()) {
    Serial.println("HX711 is ready!");
  } else {
    Serial.println("HX711 not found!");
  }

  // Set scale factor (adjust this based on your calibration)
  scale.set_scale(1000);  // This is just an example factor, adjust it

  // Perform tare (zero the scale)
  scale.tare();
  delay(2000);  // Wait for stabilization

  // Set the button pin as input with internal pull-up resistor
  pinMode(BUTTON_PIN, INPUT_PULLUP);

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

  // Check if button is pressed (active LOW)
  if (digitalRead(BUTTON_PIN) == LOW) {
    Serial.println("Button pressed! Taring scale...");
    scale.tare();  // Tare the scale when the button is pressed
    delay(500);  // Debounce delay (prevents multiple taring actions)
  }

  // If the HX711 is ready, read the weight
  if (scale.is_ready()) {
    // Get the average of 10 readings from the HX711
    long weight = scale.get_units(10);  // Average of 10 readings

    // Print the weight to Serial Monitor for debugging
    Serial.print("Weight: ");
    Serial.println(weight);

    if (prev_weight != weight) {
      prev_weight = weight;
      mqttClient.beginMessage(topic_mass);
      mqttClient.print(weight);
      mqttClient.endMessage();
    }

  } else {
    Serial.println("HX711 not found.");
  }
  delay(1000);

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