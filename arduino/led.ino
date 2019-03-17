#include <Wire.h>

// Set the color to (r,g,b). Each is a byte 0-255.
// If t is nonzero, the change happens over t/30 seconds.
// For example if t is 15 the color fades over a half-second.

void led(byte r, byte g, byte b, byte t = 0)
{
  Wire.beginTransmission(0x08);
  Wire.write((t == 0) ? 0x00 : 0x01);
  Wire.write(r);
  Wire.write(g);
  Wire.write(b);
  if (t != 0)
    Wire.write(t);
  Wire.endTransmission();
}

// Set the color to hhh, a 24-bit RGB color.
// If t is nonzero, the change happens over t/30 seconds.
// For example if t is 15 the color fades over a half-second.

void led(uint32_t hhh, byte t = 0)
{
  led(hhh >> 16, hhh >> 8, hhh, t);
}

#define TEAL    0x008080L
#define ORANGE  0xffa500L

void setup() {
  Wire.begin();
}

void loop() {
  delay(1000);
  led(TEAL, 3);
  delay(1000);
  led(ORANGE, 3);
}
