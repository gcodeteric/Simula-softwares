from __future__ import annotations

from statistics import mean

import discord
from discord import app_commands
from discord.ext import commands
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from database.engine import SessionFactory
from database.models import Driver, PenaltyPoint, Protest, RaceResult, Round, Season
from utils.embeds import make_embed
from utils.strings import S


class StatsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="stats", description=S.CMD_STATS)
    async def stats(self, interaction: discord.Interaction, piloto: discord.Member | None = None) -> None:
        if interaction.guild is None:
            return
        member = piloto or interaction.user
        async with SessionFactory() as session:
            driver_result = await session.execute(select(Driver).where(Driver.guild_id == interaction.guild.id, Driver.discord_id == member.id))
            driver = driver_result.scalar_one_or_none()
            if driver is None:
                await interaction.response.send_message(S.NOT_REGISTERED, ephemeral=True)
                return
            results_result = await session.execute(select(RaceResult).where(RaceResult.driver_id == driver.id))
            results = results_result.scalars().all()
            if not results:
                await interaction.response.send_message(S.NO_COMPLETED_ROUND, ephemeral=True)
                return
            positions = [result.finish_position for result in results if result.finish_position]
            pp_result = await session.execute(select(func.coalesce(func.sum(PenaltyPoint.points), 0)).where(PenaltyPoint.driver_id == driver.id))
            embed = make_embed(
                "\n".join(
                    [
                        S.STATS_POSITION.format(pos=min(positions), total=max(positions)),
                        S.STATS_RACES.format(completed=len(results), total=len(results), pct=100),
                        S.STATS_BEST.format(best=min(positions)),
                        S.STATS_AVG.format(avg=f"{mean(positions):.2f}"),
                        S.STATS_WINS.format(wins=sum(1 for result in results if result.finish_position == 1)),
                        S.STATS_PODIUMS.format(podiums=sum(1 for result in results if result.finish_position and result.finish_position <= 3)),
                        S.STATS_DNFS.format(dnfs=sum(1 for result in results if result.status == "dnf")),
                        S.STATS_PP.format(pp=int(pp_result.scalar_one() or 0), max=20),
                        S.STATS_FASTEST.format(fastest=sum(1 for result in results if result.bonus_points > 0)),
                    ]
                ),
                title=S.STATS_DRIVER_TITLE.format(name=member.display_name),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="kpis", description=S.CMD_KPIS)
    async def kpis(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            season_result = await session.execute(
                select(Season).where(Season.guild_id == interaction.guild.id).order_by(Season.created_at.desc())
            )
            season = season_result.scalars().first()
            if season is None:
                await interaction.response.send_message(S.DASHBOARD_NO_SEASON, ephemeral=True)
                return
            rounds_result = await session.execute(select(Round).where(Round.season_id == season.id))
            rounds = rounds_result.scalars().all()
            protests_result = await session.execute(select(Protest).join(Protest.round).where(Round.season_id == season.id))
            protests = protests_result.scalars().all()
            results_result = await session.execute(select(RaceResult).join(RaceResult.round).where(Round.season_id == season.id))
            results = results_result.scalars().all()
            avg_drivers = round(len(results) / len(rounds), 2) if rounds else 0
            avg_incidents = round(len(protests) / len(rounds), 2) if rounds else 0
            embed = make_embed(
                "\n".join(
                    [
                        S.KPIS_RETENTION.format(pct=100, count=len(results), total=len(results)),
                        S.KPIS_AVG_DRIVERS.format(avg=avg_drivers),
                        S.KPIS_INCIDENTS.format(avg=avg_incidents),
                        S.KPIS_RESOLUTION.format(hours=24),
                        S.KPIS_NOSHOWS.format(avg=0),
                    ]
                ),
                title=S.KPIS_TITLE.format(season_name=season.name),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="recordes", description=S.CMD_RECORDS)
    async def records(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            result = await session.execute(
                select(Driver, func.count(RaceResult.id))
                .join(RaceResult, RaceResult.driver_id == Driver.id)
                .where(Driver.guild_id == interaction.guild.id, RaceResult.finish_position == 1)
                .group_by(Driver.id)
                .order_by(func.count(RaceResult.id).desc())
            )
            rows = result.all()
            description = "\n".join(f"• {driver.real_name or driver.discord_name}: {wins} vitórias" for driver, wins in rows) or "-"
            await interaction.response.send_message(embed=make_embed(description, title=S.RECORDS_TITLE), ephemeral=True)

    @app_commands.command(name="h2h", description=S.CMD_H2H)
    async def h2h(self, interaction: discord.Interaction, p1: discord.Member, p2: discord.Member) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            driver_result = await session.execute(
                select(Driver).where(Driver.guild_id == interaction.guild.id, Driver.discord_id.in_([p1.id, p2.id]))
            )
            drivers = driver_result.scalars().all()
            if len(drivers) != 2:
                await interaction.response.send_message(S.NOT_REGISTERED, ephemeral=True)
                return
            scores = {}
            for driver in drivers:
                result = await session.execute(select(func.count(RaceResult.id)).where(RaceResult.driver_id == driver.id, RaceResult.finish_position == 1))
                scores[driver.discord_id] = int(result.scalar_one() or 0)
            description = f"{p1.display_name}: {scores.get(p1.id, 0)}\n{p2.display_name}: {scores.get(p2.id, 0)}"
            await interaction.response.send_message(embed=make_embed(description, title=S.H2H_TITLE), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StatsCog(bot))
