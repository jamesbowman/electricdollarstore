from machine import I2C
import time

class Dig2:
    """ DIG2 is a 2-digit 7-segment LED display """

    def __init__(self, i2, a = 0x14):
        self.i2 = i2
        self.a = a

    def raw(self, b0, b1):
        """ Set all 8 segments from the bytes b0 and b1 """ 
        self.i2.writeto(self.a, bytes((0, b0, b1)))

    def hex(self, b):
        """ Display a hex number 0-0xff """
        self.i2.writeto(self.a, bytes((1, b)))

    def dec(self, b):
        """ Display a decimal number 00-99 """
        self.i2.writeto(self.a, bytes((2, b)))

    def dp(self, p0, p1):
        """ Set the state the decimal point indicators """
        self.i2.writeto(self.a, bytes((3, (p1 << 1) | p0)))

    def brightness(self, b):
        """ Set the brightness from 0 (off) to 255 (maximum) """
        self.i2.writeto(self.a, bytes((4, b)))

def main():
    i2 = I2C(1, freq = 100000)

    d = Dig2(i2)
    for i in range(100):
        d.dec(i)
        time.sleep(.05)
