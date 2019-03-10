#!/usr/bin/env python3
import sys
import serial
import random

if __name__ == '__main__':
    nonce = bytes('BYE%d' % random.randrange(1000000000), "utf-8")
    ser = serial.Serial(sys.argv[1], 115200)
    ser.write(bytes([3,4]))
    ser.write(bytes(sys.argv[2], "utf-8") + bytes([13]))
    ser.write(b'print("' + nonce + b'")\r')
    ser.flush()
    t = b''
    while t[-1-len(nonce):] != (b'\n' + nonce):
        s = ser.read()
        sys.stdout.write(s.decode("utf-8"))
        sys.stdout.flush()
        t += s
