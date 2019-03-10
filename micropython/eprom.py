from machine import I2C
import struct

class EPROM:
    """ EPROM is a CAT24C512 512 Kbit (64 Kbyte) flash memory """
    def __init__(self, i2, a = 0x50):
        self.i2 = i2
        self.a = a

    def write(self, addr, data):
        """ Write data to EPROM, starting at address addr """
        for i in range(0, len(data), 128):
            self.i2.writeto(self.a, (
                struct.pack(">H", addr + i) +
                data[i:i + 128]))
            while self.a not in self.i2.scan():
                pass
        
    def read(self, addr, n):
        """ Read n bytes from the EPROM, starting at address addr """
        self.i2.writeto(self.a, struct.pack(">H", addr), False)
        return self.i2.readfrom(self.a, n)

text = b"""\
CHAPTER 1. Loomings.

Call me Ishmael. Some years ago-never mind how long precisely-having
little or no money in my purse, and nothing particular to interest me on
shore, I thought I would sail about a little and see the watery part of
the world."""

def main():
    i2 = I2C(1, freq = 100000)

    d = EPROM(i2)
    d.write(0, text)        # Write the block of text starting at address 0
    n = len(text)
    rd = d.read(0, n)       # Read it back
    print(rd)               # Display it
