import json
import random
import time
from typing import Any, Dict

from loguru import logger

from paho.mqtt.client import MQTTMessage, Client

from config import TOPIC_PREFIX, LATENCY_MIN_MS, LATENCY_MAX_MS, RELIABILITY_PERCENT
from utils import iso_now


ACK_TOPIC = f"{TOPIC_PREFIX}/demo/ack"

VALID_RELAY_IDS = [1, 2, 3, 4, 5, 6, 7, 8]


def _is_valid_command(payload: Dict[str, Any]) -> bool:
    code = str(payload.get("code", ""))
    # Treat 10001 as turn-on and 10002 as turn-off if present
    return code in {"10001", "10002"}


def _validate_relay_id(payload: Dict[str, Any]) -> str | None:
    try:
        relay_id = int(payload.get("relay_id"))
    except Exception:
        return "invalid relay_id"

    if relay_id not in VALID_RELAY_IDS:
        return "invalid relay_id"

    return None


def _publish_ack(client: Client, controller_id: str, relay_id: int, success: bool, error: str | None = None):
    message = {
        "code": "20001" if success else "21001",
        "controller_id": controller_id,
        "relay_id": relay_id,
        "data": "ok" if success else (error or "error"),
    }
    client.publish(ACK_TOPIC, json.dumps(message), qos=0, retain=False)
    logger.info((
        "published_ack ",
        f"topic={ACK_TOPIC} ",
        f"message={message} ",
        f"time={iso_now()}",
    ))


def handle_incoming_message(client: Client, msg: MQTTMessage):
    received_at = iso_now()

    payload_text = None
    try:
        payload_text = msg.payload.decode("utf-8")
        payload = json.loads(payload_text)
        logger.info((
            "received_message ",
            f"topic={msg.topic} ",
            f"payload={payload_text} ",
            f"time={received_at}",
        ))
    except Exception as e:
        logger.error((
            "invalid_message ",
            f"topic={msg.topic} ",
            f"payload={payload_text} ",
            f"error={str(e)} ",
            f"time={received_at}",
        ))
        return

    # Only respond to demo control commands
    if not _is_valid_command(payload):
        return

    controller_id = str(payload.get("controller_id", ""))
    relay_id_val = payload.get("relay_id")

    # Validate relay id
    error = _validate_relay_id(payload)
    if error is not None:
        try:
            relay_id_int = int(relay_id_val) if relay_id_val is not None else -1
        except Exception:
            relay_id_int = -1
        _publish_ack(client, controller_id, relay_id_int, success=False, error=error)
        return

    relay_id_int = int(relay_id_val)

    # Simulate processing latency
    latency_ms = random.randint(LATENCY_MIN_MS, max(LATENCY_MIN_MS, LATENCY_MAX_MS))
    time.sleep(latency_ms / 1000.0)

    # Simulate reliability outcome
    success_roll = random.random() * 100.0
    if success_roll <= RELIABILITY_PERCENT:
        _publish_ack(client, controller_id, relay_id_int, success=True)
    else:
        _publish_ack(client, controller_id, relay_id_int, success=False, error="temporary failure")
