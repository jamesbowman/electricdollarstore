from machine import I2C
import time

class LED:
    """ LED is an RGB LED """
    def __init__(self, i2, a = 0x08):
        self.i2 = i2
        self.a = a

    def rgb(self, r, g, b, t = 0):
        """
        Set the color to (r,g,b). Each is a byte 0-255.
        If t is nonzero, the change happens over t/30 seconds.
        For example if t is 15 the color fades over a half-second.
        """
        if t == 0:
            self.i2.writeto(self.a, bytes((0, r, g, b)))
        else:
            self.i2.writeto(self.a, bytes((1, r, g, b, t)))
        
    def hex(self, hhh, t = 0):
        """
        Set the color to hhh, a 24-bit RGB color.
        If t is nonzero, the change happens over t/30 seconds.
        For example if t is 15 the color fades over a half-second.
        """
        r = (hhh >> 16) & 0xff
        g = (hhh >> 8) & 0xff
        b = hhh & 0xff
        self.rgb(r, g, b, t)


def main():
    i2 = I2C(1, freq = 100000)

    d = LED(i2)
    TEAL    = 0x008080
    ORANGE  = 0xffa500
    while 1:
        time.sleep(1)
        d.hex(TEAL, 3)
        time.sleep(1)
        d.hex(ORANGE, 3)
