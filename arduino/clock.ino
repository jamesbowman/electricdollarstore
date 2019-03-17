#include <Wire.h>

class clock {
  int a;
public:
  int
    year;       // 2000 - 2099
  byte
    month,      // 1 - 12
    mday,       // 1 - 31
    hour,       // 0 - 24
    minute,     // 0 - 60
    second,     // 0 - 60
    weekday;    // Day of week 1-7

  void begin(byte _a = 0x68) {
    a = _a;
  }
  byte bcd(byte x) {
    return (x % 10) + 16 * (x / 10);
  }
  byte decimal(byte x) {
    return (x & 0xf) + 10 * (x >> 4);
  }
  void set() {
    Wire.beginTransmission(a);
    Wire.write(7);
    Wire.write(0);
    Wire.endTransmission();

    Wire.beginTransmission(a);
    Wire.write(0);
    Wire.write(bcd(second));
    Wire.write(bcd(minute));
    Wire.write(0x80 | bcd(hour));
    Wire.write(bcd(mday));
    Wire.write(bcd(month));
    Wire.write(weekday);
    Wire.write(bcd(year % 100));
    Wire.endTransmission();
  }
  void read() {
    Wire.beginTransmission(a);
    Wire.write(0);
    Wire.endTransmission(false);
    Wire.requestFrom(a, 7);
    second = decimal(Wire.read());
    minute = decimal(Wire.read());
    hour = decimal(Wire.read() & 0x7f);
    mday = decimal(Wire.read());
    month = decimal(Wire.read());
    weekday = decimal(Wire.read());
    year = 2000 + decimal(Wire.read());
  }
};

clock Clock;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Clock.begin();

  Clock.year    = 2019;
  Clock.month   = 4;
  Clock.mday    = 1;
  Clock.hour    = 8;
  Clock.minute  = 15;
  Clock.second  = 0;

  Clock.set();
}

void loop() {
  Clock.read();

  Serial.print(" year:");   Serial.print(Clock.year);
  Serial.print(" month:");  Serial.print(Clock.month);
  Serial.print(" mday:");   Serial.print(Clock.mday);

  Serial.print(" hour:");   Serial.print(Clock.hour);
  Serial.print(" minute:"); Serial.print(Clock.minute);
  Serial.print(" second:"); Serial.print(Clock.second);

  Serial.println();
  delay(1000);
}
