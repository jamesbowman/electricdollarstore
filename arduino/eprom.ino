#include <Wire.h>

class eprom {
  uint8_t a;
public:
  void begin(byte _a = 0x50) {
    a = _a;
  }
  void write(uint16_t addr, const byte *buf, int len) {
    Wire.beginTransmission(a);
    Wire.write(addr >> 8);
    Wire.write(addr);
    Wire.write(buf, len);
    Wire.endTransmission();
    delay(5000);
  }
  void read(byte *buf, uint16_t addr, int len) {
    Wire.beginTransmission(a);
    Wire.write(addr >> 8);
    Wire.write(addr);
    Wire.endTransmission(false);
    Wire.requestFrom(a, (uint8_t)len);
    for (int i = 0; i < len; i++)
      buf[i] = Wire.read();
  }
} EPROM;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Wire.setClock(100000L);

  EPROM.write(0, "This is a test\n", 15);
}

void loop() {
  char buf[15];
  EPROM.read(buf, 0, sizeof(buf));
  Serial.write(buf, sizeof(buf));
  delay(1000);
  for (;;);
}
