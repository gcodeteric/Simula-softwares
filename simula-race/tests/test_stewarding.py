from __future__ import annotations

from datetime import UTC, datetime

import pytest

from cogs.stewarding import can_steward_vote, vote_majority_threshold
from database.models import Driver, Guild, Protest, Round, Season, SeasonStatus


def test_vote_majority_threshold_minimum_two() -> None:
    assert vote_majority_threshold(1) == 2
    assert vote_majority_threshold(3) == 2
    assert vote_majority_threshold(5) == 3


@pytest.mark.asyncio
async def test_steward_cannot_vote_when_involved(session_factory) -> None:
    async with session_factory() as session:
        session.add(Guild(id=1, name="Guild", league_name="Liga"))
        season = Season(guild_id=1, name="Season", sim="ACC", status=SeasonStatus.ACTIVE, num_rounds=10)
        session.add(season)
        await session.flush()
        round_obj = Round(season_id=season.id, round_number=1, track_name="Spa", date_time=datetime.now(UTC))
        session.add(round_obj)
        await session.flush()
        author = Driver(guild_id=1, discord_id=10, discord_name="Author")
        accused = Driver(guild_id=1, discord_id=20, discord_name="Accused")
        neutral = Driver(guild_id=1, discord_id=30, discord_name="Neutral")
        session.add_all([author, accused, neutral])
        await session.flush()
        protest = Protest(
            guild_id=1,
            round_id=round_obj.id,
            author_driver_id=author.id,
            accused_driver_id=accused.id,
            description="Incidente",
            evidence_url="https://example.com/replay",
        )
        session.add(protest)
        await session.commit()
    assert await can_steward_vote(10, protest, 1) is False
    assert await can_steward_vote(30, protest, 1) is True
