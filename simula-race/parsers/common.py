from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ParsedResult:
    player_id: str
    player_name: str
    finish_position: int
    grid_position: int | None
    best_lap_ms: int | None
    total_time_ms: int | None
    laps_completed: int
    car_model: str | None
    status: str
    incidents: int


@dataclass(slots=True)
class ParsedRace:
    track_name: str
    sim: str
    session_type: str
    results: list[ParsedResult]
    raw_data: dict[str, Any]
