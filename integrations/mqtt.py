import json
import random
import sys
import signal

import paho.mqtt.client as mqtt

from config import MQTT_HOST, MQTT_PORT, TOPIC_PREFIX
from utils import iso_now
from services.service import handle_incoming_message


DEMO_TOPIC = f"{TOPIC_PREFIX}/demo"

def on_connect(client: mqtt.Client, _userdata, _flags, rc: int):
    if rc == 0:
        print(json.dumps({
            "event": "mqtt_connected",
            "host": MQTT_HOST,
            "port": MQTT_PORT,
            "sub": DEMO_TOPIC,
            "time": iso_now(),
        }))
        client.subscribe(DEMO_TOPIC, qos=0)
    else:
        print(json.dumps({
            "event": "mqtt_connect_failed",
            "rc": rc,
            "time": iso_now(),
        }))


def on_message(client: mqtt.Client, _userdata, msg: mqtt.MQTTMessage):
    handle_incoming_message(client, msg)


def create_client() -> mqtt.Client:
    client = mqtt.Client(client_id=f"iot-sim-{random.randint(1, 10_000_000)}", clean_session=True)
    client.enable_logger()
    client.on_connect = on_connect
    client.on_message = on_message
    client.reconnect_delay_set(min_delay=1, max_delay=30)
    return client


def setup_signal_handlers(client: mqtt.Client):
    def handle_exit(signum, _frame):
        print(json.dumps({
            "event": "shutdown",
            "signal": signum,
            "time": iso_now(),
        }))
        try:
            client.loop_stop()
            client.disconnect()
        finally:
            sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
