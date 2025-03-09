#include <ArduinoMqttClient.h>
#include <WiFiNINA.h>
#include <Adafruit_Sensor.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>
#include <DHT_U.h>
#include "HX711.h"

// YorkU network credentials
#define YORKU_SSID "AirYorkGuest"
#define YORKU_PASS ""  // Should autoconnect to AirYorkGuest as MAC address is registered

// DHT11 important values
#define DHTPIN 7
#define DHTTYPE 11

// Calibration values
#define TEMP_CAL 21     // Adjusts the temperature reading for accuracy
#define HUMID_CAL 10    // Adjusts the humidity reading for accuracy
#define SCALE_CAL 1000  // Adjusts the scale reading for accuracy

// Define HX711 pins
#define DOUT 2  // Data pin (DT)
#define CLK 3   // Clock pin (SCK)

#define BUTTON_PIN 4  // Button pin to tare the scale

// Define display pins for 7SD
#define DT 8
#define SCLK 9

// For more information, check out https://freenove.com/fnk0079
// note:If lcd1602 uses PCF8574T, IIC's address is 0x27, or lcd1602 uses PCF8574AT, IIC's address is 0x3F.
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Note: HX711 will require its own power source.  Make sure to connect all wires to a common ground to the Arduino
HX711 scale;  // Create HX711 object

char ssid[] = YORKU_SSID;  // network SSID (name)
char pass[] = YORKU_PASS;  // network password (used for WPA, or as a key for WEP)

WiFiClient wiFiClient;              // Create a wifiClient
MqttClient mqttClient(wiFiClient);  // Connect wifiClient to MqttClient

DHT_Unified dht(DHTPIN, DHTTYPE);  // Specify pin and sensor model

const char broker[] = "test.mosquitto.org";
int port = 1883;
const char topic_temp[] = "temp_value";
const char topic_humid[] = "humid_value";
const char topic_mass[] = "mass_value";

// Create an interval for sending messages (in milliseconds)
const long interval = 8000;
unsigned long prev_ms = 0;

// Values for scale measurements
long weight = 0;
long prev_weight = -1;  // Stores the value of the previous recorded weight, used to compare with the current reading

// Values for temp and humidity
float temp = 0;
float humid = 0;
float prev_temp = -1;
float prev_humid = -1;

// Create sensor events for both temp and humidity
sensors_event_t temp_event;
sensors_event_t humid_event;

// Initialize the device
void setup() {
  Serial.begin(57600);

  displayInit();  // Initialize the I2C LCD Display

  // set up DHT sensor
  dht.begin();
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);

  // Boot Up Screen
  lcd.setCursor(0, 0);
  lcd.print("Pantheon3DP");
  lcd.setCursor(0, 1);
  lcd.print("Booting up");

  // Allow some time for the HX711 to stabilize
  for (int i = 0; i < 3; i++) {
    delay(300);
    lcd.print(".");
  }
  delay(100);

  // Initialize HX711
  scale.begin(DOUT, CLK);

  scaleReady();  // Determines if the HX711 module is ready

  scale.set_scale(SCALE_CAL);  // Set scale calibration factor

  // Perform tare (zero the scale)
  scale.tare();
  delay(2000);  // Wait for stabilization

  // Set the button pin as input with internal pull-up resistor
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  wifiConnect();  // attempt to connect to Wifi network and to the MQTT broker
}

// The main body of the code, allows us to constantly run after setup
void loop() {
  mqttClient.poll();  // Sends MQTT keep alive, constantly called to keep connection alive

  if (digitalRead(BUTTON_PIN) == LOW) {
    tare();  // Tare the scale if button is pressed (pin is LOW)
  }

  // If the HX711 is ready, read the weight
  if (scale.is_ready()) {
    scaleMeasure();  // Read weight value from load cell and update value accordingly
  } else {
    Serial.println("HX711 not found.");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("HX711 not");
    lcd.setCursor(0, 1);
    lcd.print("found.");
  }
  delay(500);

  readDHT11();  // Read from DHT11 sensor and update temp and humidity values accordingly
}

// Initialize Display
void displayInit() {
  // Set up I2C LCD Display
  Serial.println("Initializing display");
  if (!i2CAddrTest(0x27)) {
    lcd = LiquidCrystal_I2C(0x3F, 16, 2);
  }
  lcd.init();       // LCD driver initialization
  lcd.backlight();  // Open the backlight

  lcd.clear();
  Serial.println("Display initialized!");
}

// Determines if the HX711 module is ready
void scaleReady() {
  lcd.clear();
  // Check if HX711 is ready
  if (scale.is_ready()) {
    Serial.println("HX711 is ready!");
    lcd.setCursor(0, 0);
    lcd.print("HX711 is");
    lcd.setCursor(0, 1);
    lcd.print("ready!");
  } else {
    Serial.println("HX711 not found!");
    lcd.setCursor(0, 0);
    lcd.print("HX711 not");
    lcd.setCursor(0, 1);
    lcd.print("found.");
  }
}

// Connects to the specified WiFi network and establishes a connection to the MQTT broker
void wifiConnect() {
  // attempt to connect to Wifi network
  Serial.print("Attempting to connect to WPA SSID: ");
  Serial.println(ssid);

  // Print setup info to LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connect to WPA:");
  lcd.setCursor(0, 1);
  lcd.print(ssid);

  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }
  Serial.println("Connected to network.\n");
  Serial.println("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  // Update LCD display
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("NWork Connected.");
  lcd.setCursor(0, 1);
  lcd.print("Connect to MQTT:");

  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed\nError Code = ");
    Serial.println(mqttClient.connectError());  // Prints the error code for debugging
    while (1)
      ;  // Keep trying until connection is successful
  }

  Serial.println("Connected to MQTT broker.\n");

  // Update LCD Display
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connected to ");
  lcd.setCursor(0, 1);
  lcd.print("MQTT Broker!");
}

// Used to test the address of the display to ensure it exists
bool i2CAddrTest(uint8_t addr) {
  Wire.begin();
  Wire.beginTransmission(addr);
  if (Wire.endTransmission() == 0) {
    return true;
  }
  return false;
}

// Print the weight to the top row of the display
void printMass(long weight) {
  lcd.setCursor(0, 0);
  lcd.print("Mass: ");
  lcd.print(weight);
  lcd.print("g");
}

// Print the temp and humidity to the bottom row of the display
void printDHT(float temp, float humid) {
  lcd.setCursor(0, 1);
  lcd.print("T:");
  lcd.print(temp, 1);
  lcd.print("C  H:");
  lcd.print(humid, 1);
  lcd.print("%");
}

// Clear the display and update with mass, temp and humidity
void updateDisplay(long weight, float temp, float humid) {
  lcd.clear();
  printMass(weight);
  printDHT(temp + TEMP_CAL, humid + HUMID_CAL);
}

void readDHT11() {
  dht.temperature().getEvent(&temp_event);
  dht.humidity().getEvent(&humid_event);

  temp = temp_event.temperature;
  humid = humid_event.relative_humidity;

  if (prev_temp != temp) {
    prev_temp = temp;

    Serial.print("Send temp to topic_temp: ");
    Serial.println(topic_temp);
    Serial.println(temp + TEMP_CAL);

    // Send message, using print to send message contents
    mqttClient.beginMessage(topic_temp);
    mqttClient.print(temp + TEMP_CAL);
    mqttClient.endMessage();

    updateDisplay(weight, temp, humid);
  }

  if (prev_humid != humid) {
    prev_humid = humid;

    Serial.print("Send humid to topic_humid: ");
    Serial.println(topic_humid);
    Serial.println(humid + HUMID_CAL);

    // Send message, using print to send message contents
    mqttClient.beginMessage(topic_humid);
    mqttClient.print(humid + HUMID_CAL);
    mqttClient.endMessage();

    updateDisplay(weight, temp, humid);
  }
}

// Tares the scale reading
void tare() {
  Serial.println("Button pressed! Taring scale...");

  // Update the LCD with Tare sequence
  lcd.clear();
  printMass(weight);
  lcd.setCursor(0, 1);
  lcd.print("Taring");
  scale.tare();  // Tare the scale when the button is pressed

  // Debounce delay (prevents multiple taring actions)
  for (int i = 0; i < 3; i++) {
    lcd.print(".");
    delay(160);
  }
  updateDisplay(weight, temp, humid);
}

// Performs the scale measruement and outputs to MQTT and the serial monitor
void scaleMeasure() {
  // Get the average of 10 readings from the HX711
  weight = scale.get_units(10);  // Average of 10 readings

  // Print the weight to Serial Monitor for debugging
  Serial.print("Weight: ");
  Serial.println(weight);

  if (prev_weight != weight) {
    prev_weight = weight;

    updateDisplay(weight, temp, humid);

    // Update weight value in application via MQTT
    mqttClient.beginMessage(topic_mass);
    mqttClient.print(weight);
    mqttClient.endMessage();
  }
}