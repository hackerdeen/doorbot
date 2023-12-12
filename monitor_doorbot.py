from paho import mqtt
import paho.mqtt.client as paho
from random import randrange
from functools import partial
import time
from datetime import datetime
import logging
import socket
from secrets import *

last_resp = 0
report_thresh = 300
MQTT_BROKER_HOST = "c9cdba1c85374f12ba682b08321a435b.s2.eu.hivemq.cloud"
MQTT_BROKER_PORT = 8883
IRCCAT = "localhost:12345"

logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s",
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def irc_send(message):
    logger.debug("sending: "+message)
    host, port = IRCCAT.split(":")
    port = int(port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((host, port))
        s.sendall(message.encode() + b"\n")
        s.close()
    except socket.timeout:
        logger.info("Timeout connecting to irccat")
    except socket.error as e:
        logger.info("Error sending IRC message (%s): %s", message, e)

def log(msg):
    logger.info(msg)
    irc_send(msg)
    
def on_msg(c, ud, msg):
    global last_resp, rep_thresh
    m = msg.payload.decode("utf-8")
    print(datetime.utcnow(), m)
    if "pong" in m:
        last_resp = time.time()
        report_thresh = 300
    if "boot" in m:
        log("Doorbot booted")
    if "ACK" in m:#
        log("Door unlocked")

def monitor():
    global last_resp, report_thresh
    c = paho.Client(client_id="monitor", userdata=None, protocol=paho.MQTTv5)
    c.username_pw_set(MQTT_BROKER_USER, MQTT_BROKER_PW)
    c.on_message = on_msg
    c.tls_set()
    c.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    c.subscribe("cmd")
    c.publish("cmd", "ping")
    c.loop_start()
    while True:
        c.publish("cmd", "ping")
        time.sleep(2)
        resp_time = time.time() - last_resp
        if last_resp and  resp_time > report_thresh:
            log( f"Haven't seen a response from doorbot for {resp_time:.0f} seconds")
            report_thresh *= 2
        time.sleep(28)
    c.loop_stop()

if __name__=="__main__":
    monitor()
