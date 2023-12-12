from umqtt.simple import MQTTClient
from machine import Pin
import ubinascii
import machine
import micropython
import time
from machine import WDT
from secrets import *

relay = Pin(22, Pin.OUT, value=0)
# Was 5 (D1) on 8266 D1 mini
w = WDT(timeout=300_000)
w.feed()

# Default MQTT server to connect to
SERVER = b"c9cdba1c85374f12ba682b08321a435b.s2.eu.hivemq.cloud"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"cmd"

c = MQTTClient(CLIENT_ID, SERVER, user=USER, password=PASSWD, port=0,
               ssl=True,
               ssl_params={'server_hostname': "c9cdba1c85374f12ba682b08321a435b.s2.eu.hivemq.cloud"})

def sub_cb(topic, msg):
    global c
    print((topic, msg))
    if msg == b"open":
        c.publish(b"cmd", b"ACK")
        print("unlocked")
        relay.value(1)
        time.sleep(30)
        relay.value(0)
        print("locked")
    elif msg == b"ping":
        c.publish(b"cmd", b"pong")

    # Subscribed messages will be delivered to this callback
c.set_callback(sub_cb)
c.connect()
c.subscribe(TOPIC)
print("Connected to %s, subscribed to %s topic" % (SERVER, TOPIC))
c.publish(b"cmd", b"booted")

try:
    while 1:
        c.wait_msg()
        w.feed()
finally:
    pass

print("Disconnected...")
time.sleep(60) #zzz
machine.reset() #try, try, try again

