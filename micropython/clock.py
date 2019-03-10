from machine import I2C
import struct
import time
import utime

class Clock:
    """ CLOCK is a HT1382 I2C/3-Wire Real Time Clock with a 32 kHz crystal """
    def __init__(self, i2, a = 0x68):
        self.i2 = i2
        self.a = a
        
    def set(self, tt = None):
        """ tt is (year, month, mday, hour, minute, second, weekday, yearday), as used
        by utime. """
        if tt is None:
            tt = utime.localtime()
        (year, month, mday, hour, minute, second, weekday, yearday) = tt
        def bcd(x):
            return (x % 10) + 16 * (x // 10)
        self.i2.writeto_mem(self.a, 7, bytes([0]))
        self.i2.writeto_mem(self.a, 0, bytes([
            bcd(second),
            bcd(minute),
            0x80 | bcd(hour),    # use 24-hour mode
            bcd(mday),
            bcd(month),
            1 + weekday,
            bcd(year % 100)]))

    def regrd(self, addr, fmt = "B"):
        b = self.i2.readfrom_mem(self.a, addr, struct.calcsize(fmt))
        return struct.unpack(fmt, b)

    def read(self):
        (ss,mm,hh,dd,MM,ww,yy) = self.regrd(0, "7B")
        def dec(x):
            return (x % 16) + 10 * (x // 16)
        return (
            2000 + dec(yy),
            dec(MM),
            dec(dd),
            dec(hh & 0x7f),
            dec(mm),
            dec(ss),
            dec(ww) - 1)

def main():
    i2 = I2C(1, freq = 100000)

    d = Clock(i2)

    # Set the clock to 2010-2-10 14:45:00
    d.set((2019, 2, 10, 14, 45, 0, 0, 1))

    while True:
        print('year=%4d month=%2d mday=%2d time=%02d:%02d:%02d weekday=%d' % d.read())
        time.sleep(1)
