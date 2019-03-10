from machine import I2C
import struct
import time

class Remote:
    """ REMOTE is a NEC IR code receiver / decoder """
    def __init__(self, i2, a = 0x60):
        self.i2 = i2
        self.a = a

    def regrd(self, addr, fmt = "B"):
        b = self.i2.readfrom_mem(self.a, addr, struct.calcsize(fmt))
        return struct.unpack(fmt, b)

    def key(self):
        """
        For the electricdollarstore IR transmitter.
        If there is a code in the queue, return its character code.
        The layout of the remote is
            
             p     c     n
             <     >    ' '
             -     +     =
             0     %     &
             1     2     3
             4     5     6
             7     8     9

        If there is no IR code in the queue, return None.
        """
        (r,) = self.regrd(0)
        if r != 0:
            return chr(r)

    def raw(self):
        """
        If there is a code in the queue, return a tuple containing the four-byte code,
        and a timestamp.
        If there is no IR code in the queue, return None.
        """

        r = self.regrd(1, "4BH")
        if r[:4] != (0xff, 0xff, 0xff, 0xff):
            age_in_ms = r[4]
            return (r[:4], time.time() - age_in_ms * .001)
        else:
            return None

def main():
    i2 = I2C(1, freq = 100000)

    d = Remote(i2)

    print("Press a remote button")
    while 1:
        k = d.key()
        if k is not None:
            print("Key     : %r" % k)
        r = d.raw()
        if r is not None:
            (code, timestamp) = r
            print("Raw code: %02x %02x %02x %02x (time %.2f)" % (code[0], code[1], code[2], code[3], timestamp))
