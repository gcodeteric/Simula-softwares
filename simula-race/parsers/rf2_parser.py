from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

from rapidfuzz import process

from parsers.common import ParsedRace, ParsedResult


def _seconds_to_ms(value: str | None) -> int | None:
    if value in {None, ""}:
        return None
    return int(float(value) * 1000)


def fuzzy_match_name(target: str, candidates: list[str]) -> str:
    best = process.extractOne(target, candidates)
    if best is None:
        return target
    return str(best[0])


def parse_rf2_xml(raw_xml: str | bytes) -> ParsedRace:
    root = ET.fromstring(raw_xml)
    race = root.find(".//Race")
    if race is None:
        raise ValueError("rf2_race_missing")
    track_name = race.findtext("Track", default="")
    drivers = race.findall("Driver")
    names = [driver.findtext("Name", default="") for driver in drivers]
    parsed_results: list[ParsedResult] = []
    for driver in drivers:
        name = driver.findtext("Name", default="")
        status = driver.findtext("FinishStatus", default="Finished").lower()
        if status == "dq":
            status = "dsq"
        elif status not in {"finished", "dnf"}:
            status = "finished"
        parsed_results.append(
            ParsedResult(
                player_id=fuzzy_match_name(name, names),
                player_name=name,
                finish_position=int(driver.findtext("Position", default="0") or 0),
                grid_position=int(driver.findtext("GridPos", default="0") or 0) or None,
                best_lap_ms=_seconds_to_ms(driver.findtext("BestLapTime")),
                total_time_ms=_seconds_to_ms(driver.findtext("FinishTime")),
                laps_completed=int(driver.findtext("Laps", default="0") or 0),
                car_model=driver.findtext("VehFile"),
                status=status,
                incidents=0,
            )
        )
    parsed_results.sort(key=lambda item: item.finish_position)
    return ParsedRace(
        track_name=track_name,
        sim="rF2",
        session_type="race",
        results=parsed_results,
        raw_data={"xml": raw_xml.decode("utf-8") if isinstance(raw_xml, bytes) else raw_xml},
    )


def parse_rf2_file(path: str | Path) -> ParsedRace:
    return parse_rf2_xml(Path(path).read_text(encoding="utf-8"))
