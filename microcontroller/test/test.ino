#define YORKU_SSID ""
#define YORKU_PASS ""

//#include "cred.h" // wifi credentials
#include <ArduinoMqttClient.h>
#include <WifiNINA.h>

int temp_sensor_inPin = 7;

char ssid[] = YORKU_SSID; // network SSID (name)
char pass[] = YORKU_PASS; // network password (used for WPA, or as a key for WEP)

WifiClient wifiClient;              // Create a wifiClient
MqttClient mqttClient(wifiClient);  // Connect wifiClient to MqttClient

// Create an interval for sending messages (in milliseconds)
const long interval = 8000;
unsigned long prev_ms = 0;

void setup() {
  Serial.begin(9600);
  while(!Serial) {
    ; // wait for serial port to connect.  Needed for native USB port only
  }

  // attempt to connect to Wifi network
  Serial.print("Attempting to connect to WPA SSID: ");
  Serial.println(ssid);
  while(WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }

  Serial.println("Connected to network.\n");
  Serial.println("Attempting to connect to the MQTT broker: "+ broker);

  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed\nError Code = "+ mqttClient.connectError());
    while(1);
  }

  Serial.println("Connected to MQTT broker.\n");
}

void loop() {
  mqttClient.poll();  // Sends MQTT keep alive, constantly called to keep connection alive

  unsigned long curr_ms = millis();

  if (curr_ms - prev_ms >= inverval) {
    prev_ms = curr_ms;

    int Rvalue = digitalRead(temp_sensor_inPin);
  }
}