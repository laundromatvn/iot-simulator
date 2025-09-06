from datetime import datetime
from zoneinfo import ZoneInfo

from config import TOPIC_PREFIX


def iso_now() -> str:
    return datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()
