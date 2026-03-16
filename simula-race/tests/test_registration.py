from __future__ import annotations

from sqlalchemy import select

from cogs.registration import get_registration_season
from database.models import Guild, Season, SeasonStatus


import pytest


@pytest.mark.asyncio
async def test_get_registration_season_returns_latest_open_season(session_factory) -> None:
    async with session_factory() as session:
        session.add(Guild(id=1, name="Guild", league_name="Liga"))
        session.add_all(
            [
                Season(guild_id=1, name="Old", sim="ACC", status=SeasonStatus.REGISTRATION, num_rounds=8),
                Season(guild_id=1, name="New", sim="ACC", status=SeasonStatus.ACTIVE, num_rounds=10),
            ]
        )
        await session.commit()
    season = await get_registration_season(1)
    assert season is not None
    assert season.name == "New"
