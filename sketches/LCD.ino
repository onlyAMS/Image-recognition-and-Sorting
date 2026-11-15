#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Common I2C address: 0x27
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
    lcd.init();
    lcd.backlight();

    lcd.setCursor(0, 0);
    lcd.print("AMS!");

    lcd.setCursor(0, 1);
    lcd.print("Arduino LCD");
}

void loop() {

}