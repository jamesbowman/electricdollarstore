#include <Wire.h>

class magnet {
  uint8_t a;
  byte status;
public:
  int16_t x, y, z;
  void begin(byte _a = 0x1c) {
    a = _a;
    regwr(0x22, 0); // CTRL_REG3 operating mode 0: continuous conversion
  }
  void regwr(byte addr, byte val) {
    Wire.beginTransmission(a);
    Wire.write(addr);
    Wire.write(val);
    Wire.endTransmission();
  }
  int16_t rd16() {
    int16_t r = Wire.read();
    r |= Wire.read() << 8;
    return r;
  }
  void read() {
    do {
      Wire.beginTransmission(a);
      Wire.write(0x27);
      Wire.endTransmission(false);
      Wire.requestFrom(a, (uint8_t)7);
      status = Wire.read();
      x = rd16();
      y = rd16();
      z = rd16();
    } while ((status & 8) == 0);
  }
};

magnet Magnet;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Magnet.begin();
}

void loop() {
  Magnet.read();
  Serial.print(Magnet.x); Serial.print(' ');
  Serial.print(Magnet.y); Serial.print(' ');
  Serial.print(Magnet.z); Serial.println();
}
