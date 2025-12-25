import logging
import pickle
from typing import Any

import requests
from django.core.cache import cache

logger = logging.getLogger(__name__)

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
MONTH = 30 * DAY
YEAR = 365 * DAY
MAX_CACHE_BYTES = 900_000


def _get_cache_payload_size(value: Any) -> int | None:
    try:
        return len(pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL))
    except Exception:
        return None


def get_from_api(url: str, cache_for: int = 60) -> Any:
    cache_key = 'duckhunt_api_' + url
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as exc:
        if "api/status" in url:
            logger.warning("Error while getting status: %s", exc)
            return {
                "bot_latency": 0,
                "shards_status": [],
                "unsharded_guilds": []
            }
        if "api/stats" in url:
            logger.warning("Error while getting stats: %s", exc)
            return {
                "members_count": 0,
                "guilds_count": 0,
                "channels_count": 0,
                "players_count": 0,
                "alive_ducks_count": 0,
                "uptime": 0,
                "current_event_name": "DOWN",
                "current_event_value": ["Bot is down", "Bot under maintenance"],
                "global_ready": False,
            }
        if "api/commands" in url:
            logger.warning("Error while getting commands: %s", exc)
            return None
        return None

    payload_size = _get_cache_payload_size(data)
    if payload_size is None or payload_size <= MAX_CACHE_BYTES:
        try:
            cache.set(cache_key, data, cache_for)
        except Exception as exc:
            logger.warning("Cache set failed for %s: %s", url, exc)

    return data
