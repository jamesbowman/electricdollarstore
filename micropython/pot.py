from machine import I2C
import struct
import time

class Pot:
    """ POT is an analog knob potentiometer """
    def __init__(self, i2, a = 0x28):
        self.i2 = i2
        self.a = a

    def raw(self):
        """
        Return the current knob rotation as a 16-bit integer.
        """
        return struct.unpack("<H", self.i2.readfrom_mem(self.a, 0, 2))[0]

    def rd(self, r):
        """
        Return the current knob rotation, scaled to the range 0 .. r
        inclusive. For example rd(100) returns a value in the range 0 to 100.
        """
        return self.i2.readfrom_mem(self.a, r, 1)[0]

def main():
    i2 = I2C(1, freq = 100000)

    d = Pot(i2)

    while True:
        percentage = d.rd(100)
        print("%3d/100   raw=%3d" % (percentage, d.raw()))
        time.sleep(.05)
