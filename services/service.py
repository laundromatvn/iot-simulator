import json
from loguru import logger

from paho.mqtt.client import MQTTMessage

from utils import iso_now


def handle_incoming_message(msg: MQTTMessage):
    received_at = iso_now()
    
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
