from machine import I2C
import struct
import time

class Temp:
    """ TEMP is an LM75B temperature sensor """
    def __init__(self, i2, a = 0x48):
        self.i2 = i2
        self.a = a

    def regrd(self, r):
        return struct.unpack(">h", self.i2.readfrom_mem(self.a, 0, 2))[0]

    def read(self):
        return (self.regrd(0) >> 5) * 0.125

def main():
    i2 = I2C(1, freq = 100000)
    print(i2.scan())
    d = Temp(i2)

    while True:
        print("%.3f C" % d.read())
        time.sleep(.05)
