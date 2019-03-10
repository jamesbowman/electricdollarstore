from machine import I2C
import time

class Beep:
    """ BEEP is a beeper """
    def __init__(self, i2, a = 0x30):
        self.i2 = i2
        self.a = a

    def beep(self, dur, note):
        """
        Play a note. 
        dur is the duration in milliseconds, 0-255.
        note is a MIDI note in the range 21-127 inclusive.
        """
        self.i2.writeto(self.a, bytes((dur, note)))

def main():
    i2 = I2C(1, freq = 100000)

    d = Beep(i2)

    for note in range(55, 127):
        print("MIDI note %d" % note)
        d.beep(100, note)
        time.sleep(.100)
