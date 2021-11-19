#!/usr/bin/env python3

import serial, time
from Adafruit_IO import Client

ser = serial.Serial('/dev/ttyUSB0')

while True:
    data = []
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)

    pmt25 = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    print("pmt25", pmt25)
    pmt10 = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
    print("pmt10", pmt10)
    time.sleep(10)