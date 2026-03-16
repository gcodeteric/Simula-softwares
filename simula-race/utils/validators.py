from __future__ import annotations

from datetime import datetime
import re
from urllib.parse import urlparse

from utils.time_utils import parse_local_datetime


HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


def validate_car_number(value: str | int) -> int:
    number = int(value)
    if number < 1 or number > 999:
        raise ValueError("car_number")
    return number


def validate_required_url(value: str) -> str:
    parsed = urlparse(value.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("url")
    return value.strip()


def validate_non_empty(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("empty")
    return cleaned


def validate_hex_color(value: str) -> str:
    cleaned = value.strip()
    if not HEX_COLOR_RE.match(cleaned):
        raise ValueError("hex_color")
    return cleaned.upper()


def validate_round_datetime(date_value: str, time_value: str, timezone_name: str) -> datetime:
    return parse_local_datetime(date_value.strip(), time_value.strip(), timezone_name)


def parse_hotlap_to_ms(value: str) -> int:
    cleaned = value.strip()
    match = re.match(r"^(?:(\d+):)?(\d{1,2})\.(\d{3})$", cleaned)
    if not match:
        raise ValueError("hotlap")
    minutes = int(match.group(1) or 0)
    seconds = int(match.group(2))
    millis = int(match.group(3))
    return (minutes * 60 + seconds) * 1000 + millis


def normalize_player_id(value: str) -> str:
    cleaned = value.strip()
    if cleaned.startswith("S") and cleaned[1:].isdigit():
        return cleaned[1:]
    return cleaned
