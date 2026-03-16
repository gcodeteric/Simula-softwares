from __future__ import annotations

import json
from pathlib import Path

from parsers.common import ParsedRace, ParsedResult
from utils.validators import normalize_player_id


ACC_CAR_MODELS = {
    0: "Porsche 991 GT3 R",
    1: "Mercedes-AMG GT3",
    2: "Ferrari 488 GT3",
    3: "Audi R8 LMS",
    4: "Lamborghini Huracán GT3",
    15: "Lexus RC F GT3",
    16: "Lamborghini Huracán GT3 Evo",
    20: "AMR V8 Vantage",
    22: "McLaren 720S GT3",
    24: "Ferrari 488 GT3 Evo",
    25: "Mercedes-AMG GT3 2020",
    29: "Lamborghini Huracán SuperTrofeo EVO2",
    30: "BMW M4 GT3",
    31: "Audi R8 LMS Evo II",
}

ACC_TRACK_NAMES = {
    "barcelona": "Circuit de Barcelona-Catalunya",
    "brands_hatch": "Brands Hatch",
    "cota": "Circuit of the Americas",
    "donington": "Donington Park",
    "hungaroring": "Hungaroring",
    "imola": "Autodromo Enzo e Dino Ferrari",
    "laguna_seca": "WeatherTech Raceway Laguna Seca",
    "misano": "Misano World Circuit",
    "monza": "Autodromo Nazionale Monza",
    "mount_panorama": "Mount Panorama Circuit",
    "nurburgring": "Nürburgring",
    "paul_ricard": "Circuit Paul Ricard",
    "silverstone": "Silverstone Circuit",
    "spa": "Circuit de Spa-Francorchamps",
    "suzuka": "Suzuka International Racing Course",
    "valencia": "Circuit Ricardo Tormo",
    "watkins_glen": "Watkins Glen International",
    "zandvoort": "Circuit Zandvoort",
    "zolder": "Circuit Zolder",
    "red_bull_ring": "Red Bull Ring",
}


def parse_acc_json(raw_json: str | bytes) -> ParsedRace:
    data = json.loads(raw_json)
    lines = data.get("sessionResult", {}).get("leaderBoardLines", [])
    parsed_results: list[ParsedResult] = []
    for position, line in enumerate(lines, start=1):
        current_driver = line.get("currentDriver", {})
        timing = line.get("timing", {})
        player_id = normalize_player_id(str(current_driver.get("playerId", "")))
        laps = int(timing.get("lapCount", 0))
        total_time = timing.get("totalTime") or None
        status = "finished"
        if total_time in (0, None) and laps < 2:
            status = "dnf"
        parsed_results.append(
            ParsedResult(
                player_id=player_id,
                player_name=f"{current_driver.get('firstName', '').strip()} {current_driver.get('lastName', '').strip()}".strip(),
                finish_position=position,
                grid_position=None,
                best_lap_ms=timing.get("bestLap") or None,
                total_time_ms=total_time,
                laps_completed=laps,
                car_model=ACC_CAR_MODELS.get(line.get("car", {}).get("carModel")),
                status=status,
                incidents=int(line.get("missingMandatoryPitstop", 0)),
            )
        )
    return ParsedRace(
        track_name=ACC_TRACK_NAMES.get(data.get("trackName", ""), data.get("trackName", "")),
        sim="ACC",
        session_type="race" if data.get("sessionType") == "R" else str(data.get("sessionType", "")).lower(),
        results=parsed_results,
        raw_data=data,
    )


def parse_acc_file(path: str | Path) -> ParsedRace:
    return parse_acc_json(Path(path).read_text(encoding="utf-8"))
