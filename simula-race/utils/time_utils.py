from __future__ import annotations

from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo


DEFAULT_TIMEZONE = "Europe/Lisbon"


def get_timezone(name: str | None) -> ZoneInfo:
    return ZoneInfo(name or DEFAULT_TIMEZONE)


def now_tz(timezone_name: str | None = None) -> datetime:
    return datetime.now(tz=get_timezone(timezone_name))


def ensure_timezone(dt: datetime, timezone_name: str | None = None) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=get_timezone(timezone_name))
    return dt.astimezone(get_timezone(timezone_name))


def to_utc(dt: datetime, timezone_name: str | None = None) -> datetime:
    return ensure_timezone(dt, timezone_name).astimezone(UTC)


def parse_local_datetime(date_value: str, time_value: str, timezone_name: str | None = None) -> datetime:
    parsed = datetime.strptime(f"{date_value} {time_value}", "%Y-%m-%d %H:%M")
    return parsed.replace(tzinfo=get_timezone(timezone_name))


def format_date_time(dt: datetime, timezone_name: str | None = None) -> tuple[str, str]:
    localized = ensure_timezone(dt, timezone_name)
    return localized.strftime("%d/%m/%Y"), localized.strftime("%H:%M")


def format_short_date_time(dt: datetime, timezone_name: str | None = None) -> tuple[str, str]:
    localized = ensure_timezone(dt, timezone_name)
    return localized.strftime("%d %b %Y"), localized.strftime("%H:%M")


def calculate_round_schedule(date_time: datetime, cooldown_hours: int, protest_deadline_h: int) -> dict[str, datetime]:
    announcement = date_time - timedelta(days=7)
    briefing = date_time - timedelta(days=2)
    reminder_day = date_time - timedelta(days=1)
    reminder_final = date_time - timedelta(hours=2)
    protests_open = date_time + timedelta(hours=cooldown_hours)
    protests_close = date_time + timedelta(hours=protest_deadline_h)
    return {
        "announcement": announcement,
        "briefing": briefing,
        "reminder_day": reminder_day,
        "reminder_final": reminder_final,
        "protests_open": protests_open,
        "protests_close": protests_close,
    }


def hours_between(start: datetime, end: datetime) -> float:
    return (ensure_timezone(end) - ensure_timezone(start)).total_seconds() / 3600.0
