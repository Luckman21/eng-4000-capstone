#include "HX711.h"

// Define HX711 pins
#define DOUT 2   // Data pin (DT)
#define CLK 3    // Clock pin (SCK)
#define BUTTON_PIN 4  // Button pin to tare the scale

// Note: HX711 will require its own power source.  Make sure to connect all wires to a common ground to the Arduino

// Create HX711 object
HX711 scale;

void setup() {
  Serial.begin(57600);
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
}

void loop() {
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
  } else {
    Serial.println("HX711 not found.");
  }

  delay(1000);  // Wait 1 second before the next reading
}