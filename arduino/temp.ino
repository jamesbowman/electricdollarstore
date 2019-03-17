#include <Wire.h>

float temp_read()
{
  Wire.requestFrom(0x48, 2);
  byte h = Wire.read();
  byte l = Wire.read();
  return ((h << 3) | (l >> 5)) * 0.125;
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
}

void loop() {
  Serial.println(temp_read());
  delay(20);
}
