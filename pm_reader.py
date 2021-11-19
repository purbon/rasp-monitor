#!/usr/bin/env python3

import serial
import time
import os
from Adafruit_IO import Client

ser = serial.Serial('/dev/ttyUSB0')
aio = Client(os.environ['ADAFRUIT_IO_USERNAME'], os.environ['ADAFRUIT_IO_KEY'])

room25feed = aio.feeds('roompmtwofive')
room10feed = aio.feeds('roompmtwoten')

while True:
    data = []
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)

    pmt25 = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    #print("pmt25", pmt25)
    aio.send_data(room25feed.key, pmt25)
    pmt10 = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
    #print("pmt10", pmt10)
    aio.send_data(room10feed.key, pmt10)
    time.sleep(10)