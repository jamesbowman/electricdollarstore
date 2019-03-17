#include <Wire.h>

class accel {
  int a;
public:
  float x, y, z;
  void begin(byte _a = 0x19) {
    a = _a;
    regwr(0x20, 0b01000111); // CTRL_REG1: 50 Hz, enable X,Y,Z
    regwr(0x23, 0b00000000); // CTRL_REG4: High resolution mode
  }
  void regwr(byte addr, byte val) {
    Wire.beginTransmission(a);
    Wire.write(addr);
    Wire.write(val);
    Wire.endTransmission();
  }
  byte regrd(byte addr) {
    Wire.beginTransmission(a);
    Wire.write(addr);
    Wire.endTransmission(false);
    Wire.requestFrom(a, 1);
    while (Wire.available() < 1)
      ;
    return Wire.read();
  }
  int16_t rd16(byte addr) {
    int16_t r = regrd(addr) | (regrd(addr + 1) << 8);
    Serial.println(r);
    return r / 16384.0;
  }
  void read() {
    while ((regrd(0x27) & 8) == 0)
      ;
    x = rd16(0x28);
    y = rd16(0x30);
    z = rd16(0x32);
  }
};

accel Accel;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Accel.begin();
}

void loop() {
  Accel.read();
  Serial.print(Accel.x); Serial.print(' ');
  Serial.print(Accel.y); Serial.print(' ');
  Serial.print(Accel.z); Serial.println();
}
