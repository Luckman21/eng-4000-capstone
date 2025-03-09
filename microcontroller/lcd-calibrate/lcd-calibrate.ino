// For more information, check out https://freenove.com/fnk0079
#include <LiquidCrystal_I2C.h>

// note:If lcd1602 uses PCF8574T, IIC's address is 0x27, or lcd1602 uses PCF8574AT, IIC's address is 0x3F.
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  displayInit();

  // Test Display
  delay(2000);
  lcd.setCursor(0, 0);
  lcd.print("0123456789ABCDEF");
  lcd.setCursor(0, 1);
  lcd.print("FEDCBA9876543210");
  delay(2000);

  // Test backlight
  lcd.backlight();  // Open the backlight
  delay(2000);

  lcd.clear();  // Test a clear
  delay(500);

  lcd.setCursor(0, 0);
  lcd.print("Testing");
  lcd.setCursor(0, 1);
  lcd.print("Complete!");
}

void loop() {
}

// Initialize Display
void displayInit() {
  // Set up I2C LCD Display
  Serial.println("Initializing display");
  if (!i2CAddrTest(0x27)) {
    lcd = LiquidCrystal_I2C(0x3F, 16, 2);
  }
  lcd.init();       // LCD driver initialization
  //lcd.backlight();  // Open the backlight

  lcd.clear();
  Serial.println("Display initialized!");
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