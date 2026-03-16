from __future__ import annotations

import json
from pathlib import Path

from parsers.common import ParsedRace, ParsedResult


def parse_iracing_json(raw_json: str | bytes) -> ParsedRace:
    data = json.loads(raw_json)
    results = []
    for index, row in enumerate(data.get("results", []), start=1):
        results.append(
            ParsedResult(
                player_id=str(row.get("cust_id", "")),
                player_name=row.get("display_name", ""),
                finish_position=int(row.get("finish_position", index)),
                grid_position=row.get("start_position"),
                best_lap_ms=row.get("best_lap_time_ms"),
                total_time_ms=row.get("total_time_ms"),
                laps_completed=int(row.get("laps_completed", 0)),
                car_model=row.get("car_name"),
                status=row.get("status", "finished"),
                incidents=int(row.get("incidents", 0)),
            )
        )
    return ParsedRace(
        track_name=data.get("track_name", ""),
        sim="iRacing",
        session_type=data.get("session_type", "race"),
        results=results,
        raw_data=data,
    )


def parse_iracing_file(path: str | Path) -> ParsedRace:
    return parse_iracing_json(Path(path).read_text(encoding="utf-8"))
