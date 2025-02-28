#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 7
#define DHTTYPE 11
#define TEMP_CAL 21 // Adjusts the temperature reading for accuracy
#define HUMID_CAL 15  // Adjusts the humidity reading for accuracy

DHT_Unified dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600); // setup baud rate
  dht.begin();

  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
}

void loop() {
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));
  }
  else {
    Serial.print(F("Temp Sensor Reading Value: "));
    Serial.print(event.temperature);
    Serial.print(F("\nAdjusted Temperature Value: "));
    Serial.print(event.temperature + TEMP_CAL);
    Serial.println(F("°C"));
  }
  // Get humidity event and print its value.
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!"));
  }
  else {
    Serial.print(F("Humid Sensor Reading Value: "));
    Serial.print(event.relative_humidity);
    Serial.print(F("\nAdjusted Humidity Value: "));
    Serial.print(event.relative_humidity + HUMID_CAL);
    Serial.println(F("%"));
  }

  delay(2000);
}