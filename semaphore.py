#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from random import seed
from random import random
from random import randint


green = 16
yellow = 20
red = 21
leds = [16,20,21]

seed(1)


GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)
GPIO.setup(green,GPIO.OUT)
GPIO.setup(yellow,GPIO.OUT)
GPIO.setup(red,GPIO.OUT)

try:
    for i in range(10):
        print("LED on "+str(i))
        led = leds[randint(0,2)]
        GPIO.output(led,GPIO.HIGH)

        time.sleep(1)
        print("LED off")
        GPIO.output(led,GPIO.LOW)
except KeyboardInterrupt:
    GPIO.cleanup() # cleanup all GPIO
