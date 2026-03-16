from __future__ import annotations

import asyncio
from collections import defaultdict
import json
from pathlib import Path
from typing import Any

import discord
from discord import app_commands
from discord.ext import commands
from sqlalchemy import delete, func, select
from sqlalchemy.orm import selectinload

from config import DATA_DIR, get_settings
from database.engine import SessionFactory
from database.models import ChannelConfig, ChannelPurpose, Driver, Guild, PointsSystem, RaceResult, ResultStatus, Round, RoundStatus, Season
from generators.image_results import generate_results_image
from generators.image_standings import generate_standings_image
from parsers.acc_parser import parse_acc_json
from parsers.common import ParsedRace, ParsedResult
from parsers.generic_parser import parse_generic_csv
from parsers.iracing_parser import parse_iracing_json
from parsers.rf2_parser import parse_rf2_xml
from utils.embeds import make_embed, make_error_embed, make_success_embed
from utils.strings import S
from utils.time_utils import format_date_time, format_short_date_time
from views.results_views import ResultsPreviewView


def parse_results_payload(filename: str, payload: bytes) -> ParsedRace:
    lower = filename.lower()
    if lower.endswith(".xml"):
        return parse_rf2_xml(payload)
    if lower.endswith(".csv"):
        return parse_generic_csv(payload)
    if lower.endswith(".json"):
        data = json.loads(payload)
        if "sessionResult" in data:
            return parse_acc_json(payload)
        if "results" in data and "track_name" in data:
            return parse_iracing_json(payload)
        return parse_generic_csv(payload)
    raise ValueError("unsupported_results_file")


def calculate_points(results: list[ParsedResult], points_system: PointsSystem) -> list[dict[str, Any]]:
    ordered = sorted(results, key=lambda item: item.finish_position)
    fastest_lap_owner = None
    fastest_lap_value = None
    for result in ordered:
        if result.best_lap_ms is None:
            continue
        if fastest_lap_value is None or result.best_lap_ms < fastest_lap_value:
            fastest_lap_value = result.best_lap_ms
            fastest_lap_owner = result.player_id
    scored_rows = []
    for result in ordered:
        base_points = 0
        if result.finish_position <= len(points_system.points_per_position):
            base_points = int(points_system.points_per_position[result.finish_position - 1])
        bonus_points = int(points_system.finish_bonus if result.status == "finished" else 0)
        if fastest_lap_owner == result.player_id:
            bonus_points += int(points_system.fastest_lap_bonus)
        scored_rows.append({"result": result, "base_points": base_points, "bonus_points": bonus_points, "final_points": base_points + bonus_points})
    return scored_rows


async def build_standings_rows(session, season_id: int, drops: int) -> list[dict[str, Any]]:
    results = await session.execute(
        select(RaceResult, Driver)
        .join(Driver, Driver.id == RaceResult.driver_id)
        .join(Round, Round.id == RaceResult.round_id)
        .where(Round.season_id == season_id)
    )
    by_driver: dict[int, dict[str, Any]] = defaultdict(lambda: {"name": "", "scores": [], "wins": 0, "podiums": 0, "best": 999})
    for race_result, driver in results.all():
        state = by_driver[driver.id]
        state["name"] = driver.real_name or driver.discord_name
        state["scores"].append(int(race_result.final_points))
        if race_result.finish_position == 1:
            state["wins"] += 1
        if race_result.finish_position and race_result.finish_position <= 3:
            state["podiums"] += 1
        if race_result.finish_position:
            state["best"] = min(state["best"], race_result.finish_position)
    table = []
    for driver_id, state in by_driver.items():
        sorted_scores = sorted(state["scores"], reverse=True)
        if drops > 0 and len(sorted_scores) > drops:
            total_points = sum(sorted_scores[:-drops])
        else:
            total_points = sum(sorted_scores)
        table.append(
            {
                "driver_id": driver_id,
                "name": state["name"],
                "points": total_points,
                "wins": state["wins"],
                "podiums": state["podiums"],
                "best": 0 if state["best"] == 999 else state["best"],
            }
        )
    table.sort(key=lambda item: (-item["points"], -item["wins"], -item["podiums"], item["best"]))
    return table


class ResultsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.settings = get_settings()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.guild is None or message.author.bot or not message.attachments:
            return
        async with SessionFactory() as session:
            result = await session.execute(
                select(ChannelConfig).where(ChannelConfig.guild_id == message.guild.id, ChannelConfig.purpose == ChannelPurpose.RESULTS_UPLOAD)
            )
            upload_channel = result.scalar_one_or_none()
            if upload_channel is None or upload_channel.channel_id != message.channel.id:
                return
        for attachment in message.attachments:
            if attachment.filename.endswith((".json", ".xml", ".csv")):
                await self.process_results_file(message, attachment)

    async def process_results_file(self, message: discord.Message, attachment: discord.Attachment) -> None:
        payload = await attachment.read()
        parsed = parse_results_payload(attachment.filename, payload)
        async with SessionFactory() as session:
            round_obj = await self._match_round(session, message.guild.id, parsed)
        preview_embed = self._build_preview_embed(parsed)
        view = ResultsPreviewView(
            author_id=message.author.id,
            on_publish=lambda interaction: self.publish_results(interaction, parsed, round_obj.id if round_obj else None),
            on_correct=self.correct_results,
            on_cancel=self.cancel_results,
        )
        await message.channel.send(embed=preview_embed, view=view)

    async def _match_round(self, session, guild_id: int, parsed: ParsedRace) -> Round | None:
        result = await session.execute(
            select(Round)
            .join(Round.season)
            .options(selectinload(Round.season).selectinload(Season.guild))
            .where(Season.guild_id == guild_id)
            .order_by(Round.date_time.desc())
        )
        rounds = result.scalars().all()
        for round_obj in rounds:
            if parsed.track_name.lower() in round_obj.track_name.lower() or round_obj.track_name.lower() in parsed.track_name.lower():
                return round_obj
        return rounds[0] if rounds else None

    def _build_preview_embed(self, parsed: ParsedRace) -> discord.Embed:
        winner = parsed.results[0].player_name if parsed.results else "-"
        best_lap_result = min((item for item in parsed.results if item.best_lap_ms is not None), key=lambda item: item.best_lap_ms or 0, default=None)
        best_lap = "-"
        best_lap_driver = "-"
        if best_lap_result and best_lap_result.best_lap_ms is not None:
            best_lap = f"{best_lap_result.best_lap_ms / 1000:.3f}s"
            best_lap_driver = best_lap_result.player_name
        return make_embed(
            S.RESULTS_DETECTED.format(
                track=parsed.track_name,
                drivers=len(parsed.results),
                winner=winner,
                best_lap=best_lap,
                best_lap_driver=best_lap_driver,
            )
        )

    async def publish_results(self, interaction: discord.Interaction, parsed: ParsedRace, round_id: int | None) -> None:
        if interaction.guild is None or round_id is None:
            return
        async with SessionFactory() as session:
            round_result = await session.execute(
                select(Round)
                .options(selectinload(Round.season).selectinload(Season.points_system), selectinload(Round.season).selectinload(Season.guild))
                .where(Round.id == round_id)
            )
            round_obj = round_result.scalar_one()
            await session.execute(delete(RaceResult).where(RaceResult.round_id == round_obj.id))
            points_system = round_obj.season.points_system
            if points_system is None:
                ps_result = await session.execute(select(PointsSystem).where(PointsSystem.guild_id == interaction.guild.id).order_by(PointsSystem.id.asc()))
                points_system = ps_result.scalar_one()
            scored_rows = calculate_points(parsed.results, points_system)
            unknown_drivers: list[str] = []
            for score_row in scored_rows:
                driver = await self._match_driver(session, interaction.guild.id, score_row["result"])
                if driver is None:
                    unknown_drivers.append(score_row["result"].player_name)
                    continue
                session.add(
                    RaceResult(
                        round_id=round_obj.id,
                        driver_id=driver.id,
                        finish_position=score_row["result"].finish_position,
                        grid_position=score_row["result"].grid_position,
                        best_lap_ms=score_row["result"].best_lap_ms,
                        total_time_ms=score_row["result"].total_time_ms,
                        laps_completed=score_row["result"].laps_completed,
                        status=ResultStatus(score_row["result"].status),
                        base_points=score_row["base_points"],
                        bonus_points=score_row["bonus_points"],
                        final_points=score_row["final_points"],
                        car_model=score_row["result"].car_model,
                        incidents=score_row["result"].incidents,
                    )
                )
            round_obj.status = RoundStatus.RESULTS_PENDING
            await session.commit()
            await self._post_results(session, interaction.guild, round_obj)
            if unknown_drivers:
                await interaction.response.send_message(
                    S.RESULTS_UNKNOWN_DRIVER.format(count=len(unknown_drivers), names="\n".join(f"• {name}" for name in unknown_drivers)),
                    ephemeral=True,
                )
                return
        await interaction.response.edit_message(embed=make_success_embed(S.SUCCESS), view=None)

    async def _match_driver(self, session, guild_id: int, parsed_result: ParsedResult) -> Driver | None:
        result = await session.execute(select(Driver).where(Driver.guild_id == guild_id))
        drivers = result.scalars().all()
        normalized_name = parsed_result.player_name.lower()
        for driver in drivers:
            if parsed_result.player_id and parsed_result.player_id in {
                driver.steam_id or "",
                driver.iracing_id or "",
                driver.rf2_id or "",
            }:
                return driver
            if normalized_name in {
                driver.discord_name.lower(),
                (driver.real_name or "").lower(),
            }:
                return driver
        return None

    async def _post_results(self, session, guild: discord.Guild, round_obj: Round) -> None:
        channel_result = await session.execute(
            select(ChannelConfig).where(ChannelConfig.guild_id == guild.id, ChannelConfig.purpose == ChannelPurpose.RESULTS)
        )
        channel_cfg = channel_result.scalar_one_or_none()
        if channel_cfg is None:
            return
        channel = guild.get_channel(channel_cfg.channel_id)
        if not isinstance(channel, discord.TextChannel):
            return
        results_result = await session.execute(
            select(RaceResult, Driver)
            .join(Driver, Driver.id == RaceResult.driver_id)
            .where(RaceResult.round_id == round_obj.id)
            .order_by(RaceResult.finish_position.asc())
        )
        rows = results_result.all()
        description_rows = []
        image_rows = []
        for index, (race_result, driver) in enumerate(rows, start=1):
            medal = S.RESULTS_MEDAL_1 if index == 1 else S.RESULTS_MEDAL_2 if index == 2 else S.RESULTS_MEDAL_3 if index == 3 else S.RESULTS_MEDAL_OTHER
            best_lap = f"{(race_result.best_lap_ms or 0) / 1000:.3f}s" if race_result.best_lap_ms else "-"
            description_rows.append(
                S.RESULTS_ROW.format(
                    pos=race_result.finish_position or index,
                    medal=medal,
                    name=driver.real_name or driver.discord_name,
                    car=race_result.car_model or "-",
                    best_lap=best_lap,
                    points=race_result.final_points,
                )
            )
            image_rows.append(
                {
                    "position": race_result.finish_position or index,
                    "number": driver.car_number or 0,
                    "name": driver.real_name or driver.discord_name,
                    "car": race_result.car_model or "-",
                    "best_lap": best_lap,
                    "points": race_result.final_points,
                }
            )
        open_date, open_time = format_short_date_time(round_obj.protests_open_at or round_obj.date_time, round_obj.season.guild.timezone)
        embed = make_embed(
            "\n".join(description_rows),
            title=S.RESULTS_PROVISIONAL.format(
                n=round_obj.round_number,
                track=round_obj.track_name,
                flag=round_obj.track_flag or "",
                protest_open=f"{open_date} {open_time}",
            ),
        )
        output = await asyncio.to_thread(
            generate_results_image,
            DATA_DIR / f"results_round_{round_obj.id}.png",
            image_rows,
            f"Ronda {round_obj.round_number}",
            round_obj.track_name,
            f"{round_obj.weather} | {round_obj.race_duration_min} min",
            round_obj.season.guild.primary_color,
            round_obj.season.guild.secondary_color,
            self.settings.font_path,
            self.settings.font_bold_path,
        )
        await channel.send(embed=embed, file=discord.File(output))

    async def correct_results(self, interaction: discord.Interaction, notes: str) -> None:
        await interaction.response.send_message(embed=make_embed(notes, title=S.RESULTS_BTN_CORRECT), ephemeral=True)

    async def cancel_results(self, interaction: discord.Interaction) -> None:
        await interaction.response.edit_message(view=None, embed=make_error_embed(S.CANCEL))

    @app_commands.command(name="resultados", description=S.CMD_RESULTS)
    async def results(self, interaction: discord.Interaction, ronda: int | None = None) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            query = (
                select(Round)
                .options(selectinload(Round.season).selectinload(Season.guild))
                .join(Round.season)
                .where(Season.guild_id == interaction.guild.id)
                .order_by(Round.round_number.desc())
            )
            if ronda is not None:
                query = query.where(Round.round_number == ronda)
            round_result = await session.execute(query)
            round_obj = round_result.scalars().first()
            if round_obj is None:
                await interaction.response.send_message(S.NO_COMPLETED_ROUND, ephemeral=True)
                return
            results_result = await session.execute(
                select(RaceResult, Driver)
                .join(Driver, Driver.id == RaceResult.driver_id)
                .where(RaceResult.round_id == round_obj.id)
                .order_by(RaceResult.finish_position.asc())
            )
            rows = results_result.all()
            description = "\n".join(
                S.RESULTS_ROW.format(
                    pos=result.finish_position or 0,
                    medal=S.RESULTS_MEDAL_OTHER,
                    name=driver.real_name or driver.discord_name,
                    car=result.car_model or "-",
                    best_lap=f"{(result.best_lap_ms or 0) / 1000:.3f}s" if result.best_lap_ms else "-",
                    points=result.final_points,
                )
                for result, driver in rows
            ) or "-"
            await interaction.response.send_message(
                embed=make_embed(description, title=S.RESULTS_FINAL.format(n=round_obj.round_number, track=round_obj.track_name, flag=round_obj.track_flag or "")),
                ephemeral=True,
            )

    @app_commands.command(name="standings", description=S.CMD_STANDINGS)
    async def standings(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            season_result = await session.execute(
                select(Season)
                .options(selectinload(Season.points_system))
                .where(Season.guild_id == interaction.guild.id)
                .order_by(Season.created_at.desc())
            )
            season = season_result.scalars().first()
            if season is None:
                await interaction.response.send_message(S.DASHBOARD_NO_SEASON, ephemeral=True)
                return
            rows = await build_standings_rows(session, season.id, season.drops)
            description_lines = [
                S.STANDINGS_ROW.format(
                    pos=index,
                    medal=S.RESULTS_MEDAL_1 if index == 1 else S.RESULTS_MEDAL_2 if index == 2 else S.RESULTS_MEDAL_3 if index == 3 else S.RESULTS_MEDAL_OTHER,
                    name=row["name"],
                    points=row["points"],
                    wins=row["wins"],
                    podiums=row["podiums"],
                    best=row["best"],
                )
                for index, row in enumerate(rows, start=1)
            ]
            image_rows = [
                {
                    "position": index,
                    "name": row["name"],
                    "points": row["points"],
                    "wins": row["wins"],
                    "podiums": row["podiums"],
                }
                for index, row in enumerate(rows, start=1)
            ]
            guild_result = await session.execute(select(Guild).where(Guild.id == interaction.guild.id))
            guild_record = guild_result.scalar_one()
            output = await asyncio.to_thread(
                generate_standings_image,
                DATA_DIR / f"standings_season_{season.id}.png",
                image_rows,
                season.name,
                S.STANDINGS_AFTER_ROUND.format(n=len(image_rows), total=season.num_rounds, drops=season.drops),
                guild_record.primary_color,
                guild_record.secondary_color,
                self.settings.font_path,
                self.settings.font_bold_path,
            )
            await interaction.response.send_message(
                embed=make_embed("\n".join(description_lines) or "-", title=S.STANDINGS_TITLE.format(season_name=season.name)),
                file=discord.File(output),
                ephemeral=True,
            )

    @app_commands.command(name="finalizar", description=S.CMD_FINALIZE)
    async def finalize(self, interaction: discord.Interaction, ronda: int) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            round_result = await session.execute(
                select(Round)
                .join(Round.season)
                .where(Round.round_number == ronda, Season.guild_id == interaction.guild.id)
                .order_by(Round.date_time.desc())
            )
            round_obj = round_result.scalars().first()
            if round_obj is None:
                await interaction.response.send_message(S.NO_COMPLETED_ROUND, ephemeral=True)
                return
            round_obj.status = RoundStatus.FINISHED
            round_obj.final_results_at = func.now()
            await session.commit()
        await interaction.response.send_message(embed=make_success_embed(S.SUCCESS), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ResultsCog(bot))
