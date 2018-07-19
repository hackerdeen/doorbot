#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

pin = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, 1)
sleep(10)
GPIO.output(pin, 0)

