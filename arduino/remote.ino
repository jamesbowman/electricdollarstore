#include <Wire.h>

char remote_read()
{
  Wire.beginTransmission(0x60);
  Wire.write(0);
  Wire.endTransmission(false);
  Wire.requestFrom(0x60, 1);
  return Wire.read();
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
}

void loop() {
  char k = remote_read();
  if (k)
    Serial.println(k);
}
