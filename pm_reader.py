#!/usr/bin/env python3

import sys
import serial
import time
from datetime import datetime
import os
from Adafruit_IO import Client, Feed
import Adafruit_DHT

ser = serial.Serial('/dev/ttyUSB0')

def send(aio, pmt25, pmt10, temp, humidity):
    print("sending data")

    room25feed = aio.feeds('roompmtwofive')
    room10feed = aio.feeds('roompmtwoten')
    roomTempFeed = aio.feeds('roomtemp')
    roomHumFeed = aio.feeds('roomhumidity')

    aio.send_data(room25feed.key, pmt25)
    aio.send_data(room10feed.key, pmt10)
    aio.send_data(roomTempFeed.key, temperature)
    aio.send_data(roomHumFeed.key, humidity)

def save(file, pmt25, pmt10, temp, humidity):
    print("saving data in file")

def echo(dt, pmt25, pmt10, temp, humidity):
    print("%2d, %2d, %2d, %2d, %2d" % (dt.microsecond, pmt25, pmt10, temp, humidity))

if __name__ == "__main__":
    aio = None
    if len(sys.argv) > 2:
        mode = sys.argv[1] # First param, would be modus in lower case
        store = sys.argv[2] # Store mode (send, for ada IO, store for file)
    else:
        aio = Client(os.environ['ADAFRUIT_IO_USERNAME'], os.environ['ADAFRUIT_IO_KEY'])
        mode = "all"

    print("Time, pmt25, pmt10, temparature, humidity")

    while True:
        data = []
        for index in range(0, 10):
            datum = ser.read()
            data.append(datum)

        pmt25 = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
        pmt10 = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

        humidity = -1
        temperature = -1

        if mode == "all":
            humidity, temperature = Adafruit_DHT.read_retry(11, 4)

        dt = datetime.now()
        echo(dt, pmt25, pmt10, temperature, humidity)

        time.sleep(60)
