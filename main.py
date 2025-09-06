import json

from config import (
    MQTT_HOST, MQTT_PORT,
    TOPIC_PREFIX,
    LATENCY_MIN_MS,
    LATENCY_MAX_MS,
    RELIABILITY_PERCENT,
)
from utils import iso_now
from integrations.mqtt import create_client, setup_signal_handlers


DEMO_TOPIC = f"{TOPIC_PREFIX}/demo"

if __name__ == "__main__":
    client = create_client()
    setup_signal_handlers(client)
    print(json.dumps({
        "event": "starting",
        "mqttHost": MQTT_HOST,
        "mqttPort": MQTT_PORT,
        "topic": DEMO_TOPIC,
        "latencyMinMs": LATENCY_MIN_MS,
        "latencyMaxMs": LATENCY_MAX_MS,
        "reliabilityPercent": RELIABILITY_PERCENT,
        "time": iso_now(),
    }))
    client.connect(MQTT_HOST, MQTT_PORT, keepalive=30)
    client.loop_forever()
