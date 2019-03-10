from machine import I2C
import struct
import time

class Accel:
    """ ACCEL is a Richtek RT3000C 3-Axis Digital Accelerometer """

    def __init__(self, i2, a = 0x19):
        self.i2 = i2
        self.a = a
        self.regwr(0x20, 0b01000111) # CTRL_REG1: 50 Hz, enable X,Y,Z
        self.regwr(0x23, 0b00000000) # CTRL_REG4: High resolution mode

    def regwr(self, memaddr, val):
        self.i2.writeto(self.a, bytes((memaddr, val)))

    def regrd(self, memaddr):
        return self.i2.readfrom_mem(self.a, memaddr, 1)[0]

    def measurement(self):
        """ Wait for a new reading, return the (x,y,z) acceleration in g """

        # Note that the RT3000A does not support multibyte
        # reads. So must read the data one byte at a time.

        while True:
            STS_REG = self.regrd(0x27)
            if STS_REG & 8:
                regs = [self.regrd(i) for i in range(0x28, 0x2e)]
                xyz = struct.unpack("<3h", bytes(regs))
                return tuple([c / 16384. for c in xyz])

def main():
    i2 = I2C(1, freq = 100000)

    d = Accel(i2)

    while 0:
        print(d.regrd(0x27))
        time.sleep(1)

    while True:
        print("x=%+.3f  y=%+.3f  z=%+.3f" % d.measurement())
