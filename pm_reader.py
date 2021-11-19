#!/usr/bin/env python3

import serial
import time
import os
from Adafruit_IO import Client, Feed
import Adafruit_DHT

ser = serial.Serial('/dev/ttyUSB0')
aio = Client(os.environ['ADAFRUIT_IO_USERNAME'], os.environ['ADAFRUIT_IO_KEY'])

#feed1 = Feed(name='roompmtwofive')
#result1 = aio.create_feed(feed1)
#feed2 = Feed(name='roompmtwoten')
#result2 = aio.create_feed(feed2)

room25feed = aio.feeds('roompmtwofive')
room10feed = aio.feeds('roompmtwoten')
roomTempFeed = aio.feeds('roomtemp')
roomHumFeed = aio.feeds('roomhumidity')

while True:
    data = []
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)

    pmt25 = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    aio.send_data(room25feed.key, pmt25)
    pmt10 = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
    aio.send_data(room10feed.key, pmt10)

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    #print("h", humidity, "t", temperature)
    aio.send_data(roomTempFeed.key, temperature)
    aio.send_data(roomHumFeed.key, humidity)

    time.sleep(60)
