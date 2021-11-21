#!/usr/bin/env python3

import sys
import serial
import time
from datetime import datetime
import os
from Adafruit_IO import Client, Feed
import Adafruit_DHT
import atexit

ser = serial.Serial('/dev/ttyUSB0')


class AdaFruitStore:

    def __init__(self):
        self.aio = Client(os.environ['ADAFRUIT_IO_USERNAME'], os.environ['ADAFRUIT_IO_KEY'])
        self.room25feed = self.aio.feeds('roompmtwofive')
        self.room10feed = self.aio.feeds('roompmtwoten')
        self.roomTempFeed = self.aio.feeds('roomtemp')
        self.roomHumFeed = self.aio.feeds('roomhumidity')

    def header(self):
        pass

    def close(self):
        pass

    def save(self, dt, pmt25, pmt10, temperature, humidity):
        print("sending data")
        self.aio.send_data(self.room25feed.key, pmt25)
        self.aio.send_data(self.room10feed.key, pmt10)
        self.aio.send_data(self.roomTempFeed.key, temperature)
        self.aio.send_data(self.roomHumFeed.key, humidity)


class FileStore:

    def __init__(self):
        self.file = open("pm.log", "a+")

    def save(self, dt, pmt25, pmt10, temp, humidity):
        line = "{}, {:2f}, {:2f}, {:2f}, {:2f}\n".format(dt.timestamp(), pmt25, pmt10, temp, humidity)
        self.file.write(line)
        self.file.flush()

    def header(self):
        self.file.write("time, pmt25, pmt10, temparature, humidity\n")

    def close(self):
        self.file.close()


def close(metrics_store):
    metrics_store.close()


if __name__ == "__main__":

    if len(sys.argv) > 2:
        mode = sys.argv[1]  # First param, would be modus in lower case
        store = sys.argv[2]  # Store mode (send, for ada IO, store for file)
    else:
        mode = "all"
        store = "file"

    if store == "ada":
        store = AdaFruitStore()
    else:
        store = FileStore()

    atexit.register(close, metrics_store=store)
    store.header()

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
        store.save(dt, pmt25, pmt10, temperature, humidity)

        time.sleep(60)
