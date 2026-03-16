from __future__ import annotations

import csv
import io
from pathlib import Path

from parsers.common import ParsedRace, ParsedResult


def time_to_ms(value: str) -> int | None:
    cleaned = value.strip()
    if not cleaned:
        return None
    if ":" not in cleaned:
        return int(float(cleaned) * 1000)
    parts = cleaned.split(":")
    if len(parts) == 2:
        minutes = int(parts[0])
        seconds, millis = parts[1].split(".")
        return (minutes * 60 + int(seconds)) * 1000 + int(millis.ljust(3, "0")[:3])
    if len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds, millis = parts[2].split(".")
        return ((hours * 3600) + (minutes * 60) + int(seconds)) * 1000 + int(millis.ljust(3, "0")[:3])
    raise ValueError("time_format")


def parse_generic_csv(raw_csv: str | bytes, track_name: str = "Manual") -> ParsedRace:
    text = raw_csv.decode("utf-8") if isinstance(raw_csv, bytes) else raw_csv
    reader = csv.DictReader(io.StringIO(text))
    results: list[ParsedResult] = []
    for row in reader:
        results.append(
            ParsedResult(
                player_id=row.get("driver_name", "").strip(),
                player_name=row.get("driver_name", "").strip(),
                finish_position=int(row.get("position", "0") or 0),
                grid_position=None,
                best_lap_ms=time_to_ms(row.get("best_lap", "")),
                total_time_ms=time_to_ms(row.get("total_time", "")),
                laps_completed=int(row.get("laps", "0") or 0),
                car_model=row.get("car"),
                status=row.get("status", "finished").lower(),
                incidents=int(row.get("incidents", "0") or 0),
            )
        )
    results.sort(key=lambda item: item.finish_position)
    return ParsedRace(track_name=track_name, sim="Generic", session_type="race", results=results, raw_data={"csv": text})


def parse_generic_file(path: str | Path, track_name: str = "Manual") -> ParsedRace:
    return parse_generic_csv(Path(path).read_text(encoding="utf-8"), track_name=track_name)
