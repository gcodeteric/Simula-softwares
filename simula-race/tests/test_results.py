from __future__ import annotations

from datetime import UTC, datetime

import pytest
from sqlalchemy import select

from cogs.results import build_standings_rows, calculate_points
from database.models import Driver, Guild, PointsSystem, RaceResult, ResultStatus, Round, Season, SeasonStatus
from parsers.common import ParsedResult


def test_calculate_points_applies_fastest_lap_bonus() -> None:
    points_system = PointsSystem(
        name="Teste",
        points_per_position=[25, 18, 15],
        fastest_lap_bonus=1,
        finish_bonus=0,
    )
    results = [
        ParsedResult("1", "Ana", 1, None, 120000, 1800000, 20, "BMW", "finished", 0),
        ParsedResult("2", "Bruno", 2, None, 119000, 1805000, 20, "Ferrari", "finished", 0),
    ]
    rows = calculate_points(results, points_system)
    assert rows[0]["final_points"] == 25
    assert rows[1]["final_points"] == 19


@pytest.mark.asyncio
async def test_build_standings_rows_applies_drops(session_factory) -> None:
    async with session_factory() as session:
        guild = Guild(id=1, name="Guild", league_name="Liga")
        points_system = PointsSystem(guild_id=1, name="Teste", points_per_position=[25, 18, 15])
        season = Season(guild_id=1, name="Season 1", sim="ACC", status=SeasonStatus.ACTIVE, num_rounds=3, drops=1)
        session.add_all([guild, points_system, season])
        await session.flush()
        season.points_system_id = points_system.id
        driver_1 = Driver(guild_id=1, discord_id=1, discord_name="Ana")
        driver_2 = Driver(guild_id=1, discord_id=2, discord_name="Bruno")
        session.add_all([driver_1, driver_2])
        await session.flush()
        round_1 = Round(season_id=season.id, round_number=1, track_name="Spa", date_time=datetime.now(UTC))
        round_2 = Round(season_id=season.id, round_number=2, track_name="Monza", date_time=datetime.now(UTC))
        session.add_all([round_1, round_2])
        await session.flush()
        session.add_all(
            [
                RaceResult(round_id=round_1.id, driver_id=driver_1.id, finish_position=1, status=ResultStatus.FINISHED, final_points=25),
                RaceResult(round_id=round_2.id, driver_id=driver_1.id, finish_position=5, status=ResultStatus.FINISHED, final_points=5),
                RaceResult(round_id=round_1.id, driver_id=driver_2.id, finish_position=2, status=ResultStatus.FINISHED, final_points=18),
                RaceResult(round_id=round_2.id, driver_id=driver_2.id, finish_position=2, status=ResultStatus.FINISHED, final_points=18),
            ]
        )
        await session.commit()
        rows = await build_standings_rows(session, season.id, drops=1)
        assert rows[0]["name"] == "Ana"
        assert rows[0]["points"] == 25
