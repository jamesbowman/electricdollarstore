#include <Wire.h>

byte pot_read(byte scale)
{
  Wire.beginTransmission(0x28);
  Wire.write(scale);
  Wire.endTransmission(false);
  Wire.requestFrom(0x28, 1);
  return Wire.read();
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
}

void loop() {
  Serial.println(pot_read(100));
  delay(20);
}
