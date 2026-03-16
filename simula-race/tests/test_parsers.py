from __future__ import annotations

from pathlib import Path

from parsers.acc_parser import parse_acc_file
from parsers.generic_parser import parse_generic_file
from parsers.iracing_parser import parse_iracing_json
from parsers.rf2_parser import parse_rf2_file


FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_acc_fixture() -> None:
    race = parse_acc_file(FIXTURES / "acc_result_sample.json")
    assert race.sim == "ACC"
    assert race.track_name == "Circuit de Spa-Francorchamps"
    assert len(race.results) == 2
    assert race.results[0].player_id == "76561198000000001"
    assert race.results[0].car_model == "BMW M4 GT3"


def test_parse_rf2_fixture() -> None:
    race = parse_rf2_file(FIXTURES / "rf2_result_sample.xml")
    assert race.sim == "rF2"
    assert race.track_name == "Spa-Francorchamps"
    assert race.results[0].finish_position == 1
    assert race.results[0].best_lap_ms == 138234


def test_parse_generic_fixture() -> None:
    race = parse_generic_file(FIXTURES / "csv_result_sample.csv", track_name="Monza")
    assert race.track_name == "Monza"
    assert race.results[1].status == "finished"
    assert race.results[0].best_lap_ms == 138456


def test_parse_iracing_inline() -> None:
    race = parse_iracing_json(
        {
            "track_name": "Suzuka",
            "session_type": "race",
            "results": [
                {
                    "cust_id": 101,
                    "display_name": "Ana Costa",
                    "finish_position": 1,
                    "start_position": 2,
                    "best_lap_time_ms": 123456,
                    "total_time_ms": 1800000,
                    "laps_completed": 20,
                    "car_name": "BMW M4 GT3",
                    "status": "finished",
                    "incidents": 3,
                }
            ],
        }.__str__().replace("'", "\"")
    )
    assert race.sim == "iRacing"
    assert race.results[0].player_name == "Ana Costa"
