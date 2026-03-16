from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
DEFAULT_SQLITE_PATH = DATA_DIR / "league.db"


def _normalize_runtime_database_url(raw_url: str) -> str:
    if raw_url.startswith("sqlite+aiosqlite://"):
        return raw_url
    if raw_url.startswith("sqlite:///"):
        return raw_url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    if raw_url.startswith("postgresql://"):
        return raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return raw_url


def _normalize_alembic_database_url(raw_url: str) -> str:
    if raw_url.startswith("sqlite+aiosqlite:///"):
        return raw_url.replace("sqlite+aiosqlite:///", "sqlite:///", 1)
    if raw_url.startswith("postgresql+asyncpg://"):
        return raw_url.replace("postgresql+asyncpg://", "postgresql://", 1)
    return raw_url


@dataclass(frozen=True)
class Settings:
    discord_bot_token: str | None
    guild_id: int | None
    log_level: str
    timezone: str
    font_path: str
    font_bold_path: str
    raw_database_url: str
    runtime_database_url: str
    alembic_database_url: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    load_dotenv(ROOT_DIR / ".env")

    token = os.getenv("DISCORD_BOT_TOKEN") or os.getenv("DISCORD_TOKEN")
    database_url = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}")
    guild_id = os.getenv("GUILD_ID")

    return Settings(
        discord_bot_token=token,
        guild_id=int(guild_id) if guild_id else None,
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        timezone=os.getenv("TIMEZONE", "Europe/Lisbon"),
        font_path=os.getenv(
            "FONT_PATH",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ),
        font_bold_path=os.getenv(
            "FONT_BOLD_PATH",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ),
        raw_database_url=database_url,
        runtime_database_url=_normalize_runtime_database_url(database_url),
        alembic_database_url=_normalize_alembic_database_url(database_url),
    )
