from machine import I2C
import struct
import time

class Magnet:
    """ MAGNET is an ST LIS3MDL 3-axis magnetometer """
    def __init__(self, i2, a = 0x1c):
        self.i2 = i2
        self.a = a
        self.regwr(0x22, 0) # CTRL_REG3 operating mode 0: continuous conversion

    def regwr(self, memaddr, val):
        self.i2.writeto(self.a, bytes((memaddr, val)))

    def rd(self):
        """ Read the measurement STATUS_REG and OUT_X,Y,Z """
        return struct.unpack("<B3h", self.i2.readfrom_mem(self.a, 0x27, 7))

    def measurement(self):
        """ Wait for a new field reading, return the (x,y,z) """
        while True:
            (status, x, y, z) = self.rd()
            if status & 8:
                return (x, y, z)


def main():
    i2 = I2C(1, freq = 100000)

    d = Magnet(i2)

    while True:
        print(d.measurement())
