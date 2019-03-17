#include <Wire.h>

void dig2_show(byte v, int m = DEC)
{
  Wire.beginTransmission(0x14);
  Wire.write((m == HEX) ? 1 : 2);
  Wire.write(v);
  Wire.endTransmission();
}

void setup() {
  Wire.begin();
}

int i;
void loop() {
  dig2_show(i++);
  delay(100);
}
