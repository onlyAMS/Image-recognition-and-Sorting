#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

Servo myServo;

// Common I2C address: 0x27
LiquidCrystal_I2C lcd(0x27, 16, 2);


void setup() {
    lcd.init();
    lcd.backlight();
    Serial.begin(9600);
    myServo.attach(6);

    lcd.setCursor(0, 0);
    lcd.print("AMS!");


}

void loop() {

    if (Serial.available() > 0){

    String data = Serial.readStringUntil('\n');
    data.trim();
  // using an if statement here seems to have a different effect
    if (data == "red"){
    lcd.clear();
    lcd.setCursor(0, 1);
    lcd.print(data);
    myServo.write(0);
    Serial.println("DONE!!");
  }
  if (data == "blue"){
    lcd.clear();
    lcd.setCursor(0, 1);
    lcd.print(data);
    myServo.write(90);
    Serial.println("DONE!!");
  }
  if (data == "green"){
    lcd.clear();
    lcd.setCursor(0, 1);
    lcd.print(data);
    myServo.write(180);
    Serial.println("DONE!!");
  }
  }
    }