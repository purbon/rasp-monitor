#!/usr/bin/env python3

import serial
import time
import os
from Adafruit_IO import Client, Feed
import Adafruit_DHT

ser = serial.Serial('/dev/ttyUSB0')
aio = Client(os.environ['ADAFRUIT_IO_USERNAME'], os.environ['ADAFRUIT_IO_KEY'])

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

def echo(pmt25, pmt10, temp, humidity):
    print(f'{pmt25:.2f}, {pmt10:.2f}, {temp:.2f}, {humidity:.2f}')

if __name__ == "__main__":
    if len(sys.argv) > 2:
        mode = sys.argv[1] # First param, would be modus in lower case
        store = sys.argv[2] # Store mode (send, for ada IO, store for file)
    else:
        mode = "all"

    while True:
        data = []
        for index in range(0, 10):
            datum = ser.read()
            data.append(datum)

        pmt25 = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
        pmt10 = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

        humidity = None
        temperature = None

        if mode == "all":
            humidity, temperature = Adafruit_DHT.read_retry(11, 4)

        echo(pmt25, pmt10, temp, humidity)

        time.sleep(60)
