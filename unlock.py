#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
import paho.mqtt.client as mqtt
# import the secrets from config.py, not committed to the repo
import config
# Config's layout looks like this:
#MQTT_CONFIG = {
#    'host': 'aaa.bbb.ccc.ddd',
#    'user': 'username',
#    'pass': 'pasword'
#}

#set up mqtt optoins
mqttc = mqtt.Client()
mqttc.username_pw_set(config.MQTT_CONFIG['user'], config.MQTT_CONFIG['pass'])

pin = 26

# Set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
# Unlock Door
GPIO.output(pin, 1)
# connect to mqtt
mqttc.connect(config.MQTT_CONFIG['host'])
# publish to space/status topic, unlocked will trigger the relevant script in
# hass
infot = mqttc.publish("space/status", "unlocked")
mqttc.disconnect()
sleep(10)
# Lock Door
GPIO.output(pin, 0)
