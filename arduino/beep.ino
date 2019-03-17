#include <Wire.h>

void beep(byte dur, byte note)
{
  Wire.beginTransmission(0x30);
  Wire.write(dur);
  Wire.write(note);
  Wire.endTransmission();
}

void setup() {
  Wire.begin();
}

void loop() {
  for (int note = 55; note < 127; note++) {
    beep(100, note);
    delay(100);
  }
}
