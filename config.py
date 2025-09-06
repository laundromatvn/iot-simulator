import os


# MQTT configuration
MQTT_HOST = os.getenv("MQTT_HOST", "27.71.26.189")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

# Topics and simulator behavior configuration
TOPIC_PREFIX = os.getenv("TOPIC_PREFIX", "lms/").strip("/")
LATENCY_MIN_MS = int(os.getenv("LATENCY_MIN_MS", "200"))
LATENCY_MAX_MS = int(os.getenv("LATENCY_MAX_MS", "600"))
RELIABILITY_PERCENT = float(os.getenv("RELIABILITY_PERCENT", "95"))
