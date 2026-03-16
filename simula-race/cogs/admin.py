from __future__ import annotations

import json
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from sqlalchemy import delete, select

from config import DATA_DIR
from database.engine import SessionFactory
from database.models import ChannelConfig, ChannelPurpose, Division, Guild, PointsSystem, Round, Season, SeasonStatus, StaffMember, StaffRole
from utils.embeds import make_embed, make_error_embed, make_success_embed
from utils.strings import S
from utils.time_utils import calculate_round_schedule, format_date_time
from views.round_wizard import RoundState, RoundWizardStep1, round_created_embed
from views.season_wizard import SeasonState, SeasonWizardStep1
from views.setup_wizard import SetupState, SetupWizardStep1


def load_points_system_definitions() -> list[dict[str, object]]:
    payload = json.loads((DATA_DIR / "points_systems.json").read_text(encoding="utf-8"))
    return [
        {
            "slug": slug,
            "id": index,
            "name": item["name"],
            "description": item["description"],
            "points_per_position": item["points_per_position"],
            "pole_bonus": item["pole_bonus"],
            "fastest_lap_bonus": item["fastest_lap_bonus"],
            "finish_bonus": item["finish_bonus"],
        }
        for index, (slug, item) in enumerate(payload.items(), start=1)
    ]


def load_tracks() -> list[dict[str, object]]:
    return json.loads((DATA_DIR / "tracks.json").read_text(encoding="utf-8"))


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="setup", description=S.CMD_SETUP)
    async def setup_wizard(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            return
        if interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message(embed=make_error_embed(S.ONLY_OWNER_SETUP), ephemeral=True)
            return
        async with SessionFactory() as session:
            result = await session.execute(select(Guild).where(Guild.id == interaction.guild.id))
            guild_record = result.scalars().first()
            if guild_record and guild_record.setup_complete:
                await interaction.response.send_message(embed=make_error_embed(S.SETUP_ALREADY_DONE), ephemeral=True)
                return
        embed = make_embed(S.SETUP_WELCOME, title=S.BOT_NAME)
        view = SetupWizardStep1(interaction.user.id, self.complete_setup)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    async def complete_setup(self, interaction: discord.Interaction, state: SetupState) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            guild_record = Guild(
                id=interaction.guild.id,
                name=interaction.guild.name,
                league_name=state.league_name,
                timezone=state.timezone,
                default_sim=state.sim,
                primary_color=state.primary_color,
                secondary_color=state.secondary_color,
                setup_complete=True,
            )
            await session.merge(guild_record)
            await session.execute(delete(ChannelConfig).where(ChannelConfig.guild_id == interaction.guild.id))
            for points_system in load_points_system_definitions():
                session.add(
                    PointsSystem(
                        guild_id=interaction.guild.id,
                        name=str(points_system["name"]),
                        points_per_position=list(points_system["points_per_position"]),
                        pole_bonus=int(points_system["pole_bonus"]),
                        fastest_lap_bonus=int(points_system["fastest_lap_bonus"]),
                        finish_bonus=int(points_system["finish_bonus"]),
                    )
                )
            session.add(StaffMember(guild_id=interaction.guild.id, discord_id=interaction.user.id, role=StaffRole.ADMIN))
            await session.commit()
            await self._create_roles(interaction.guild)
            await self._create_channels(interaction.guild)
        await interaction.response.edit_message(
            embed=make_success_embed(S.SETUP_COMPLETE.format(league_name=state.league_name)),
            view=None,
        )

    async def _create_roles(self, guild: discord.Guild) -> None:
        for role_name in S.ROLE_NAME_MAP.values():
            if discord.utils.get(guild.roles, name=role_name) is None:
                await guild.create_role(name=role_name)

    async def _create_channels(self, guild: discord.Guild) -> None:
        async with SessionFactory() as session:
            for purpose_value, channel_name in S.CHANNEL_PURPOSES.items():
                channel = discord.utils.get(guild.text_channels, name=channel_name)
                if channel is None:
                    channel = await guild.create_text_channel(channel_name)
                session.add(ChannelConfig(guild_id=guild.id, purpose=ChannelPurpose(purpose_value), channel_id=channel.id))
            await session.commit()

    async def start_season_wizard(self, interaction: discord.Interaction) -> None:
        points_systems = await self._fetch_points_systems(interaction.guild.id)
        view = SeasonWizardStep1(interaction.user.id, self.complete_season, points_systems)
        await interaction.response.edit_message(embed=make_embed(S.SEASON_STEP_NAME, title=S.SEASON_WIZARD_TITLE), view=view)

    async def complete_season(self, interaction: discord.Interaction, state: SeasonState) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            season = Season(
                guild_id=interaction.guild.id,
                name=state.name,
                sim=state.sim,
                status=SeasonStatus.DRAFT,
                num_rounds=state.num_rounds,
                drops=state.drops,
                points_system_id=state.points_system_id,
            )
            session.add(season)
            await session.flush()
            session.add(Division(season_id=season.id, name=S.DEFAULT_DIVISION_NAME, tier=1))
            await session.commit()
        await interaction.response.edit_message(
            embed=make_success_embed(
                S.SEASON_CREATED.format(
                    name=state.name,
                    sim=state.sim,
                    rounds=state.num_rounds,
                    drops=state.drops,
                    points=state.points_system_name,
                )
            ),
            view=None,
        )

    async def start_round_wizard(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            season_result = await session.execute(
                select(Season)
                .where(Season.guild_id == interaction.guild.id)
                .order_by(Season.created_at.desc())
            )
            season = season_result.scalars().first()
            guild_result = await session.execute(select(Guild).where(Guild.id == interaction.guild.id))
            guild_record = guild_result.scalars().first()
            if season is None or guild_record is None:
                await interaction.response.send_message(S.DASHBOARD_NO_SEASON, ephemeral=True)
                return
            used_rounds = await session.execute(select(Round.round_number).where(Round.season_id == season.id))
            used_numbers = set(used_rounds.scalars().all())
        available_numbers = [number for number in range(1, season.num_rounds + 1) if number not in used_numbers]
        view = RoundWizardStep1(
            interaction.user.id,
            self.complete_round,
            available_numbers,
            load_tracks(),
            guild_record.timezone,
        )
        await interaction.response.edit_message(embed=make_embed(S.ROUND_STEP_NUMBER, title=S.ROUND_WIZARD_TITLE), view=view)

    async def complete_round(self, interaction: discord.Interaction, state: RoundState) -> None:
        if interaction.guild is None or state.round_number is None or state.date_time is None:
            return
        async with SessionFactory() as session:
            season_result = await session.execute(
                select(Season)
                .where(Season.guild_id == interaction.guild.id)
                .order_by(Season.created_at.desc())
            )
            season = season_result.scalars().first()
            guild_result = await session.execute(select(Guild).where(Guild.id == interaction.guild.id))
            guild_record = guild_result.scalar_one()
            if season is None:
                await interaction.response.send_message(S.DASHBOARD_NO_SEASON, ephemeral=True)
                return
            round_obj = Round(
                season_id=season.id,
                round_number=state.round_number,
                track_name=state.track_name,
                track_country=state.track_country,
                track_flag=state.track_flag,
                format=state.format,
                start_type=state.start_type,
                race_duration_min=state.race_duration_min,
                weather=state.weather,
                date_time=state.date_time,
            )
            schedule_map = calculate_round_schedule(state.date_time, guild_record.cooldown_hours, guild_record.protest_deadline_h)
            round_obj.protests_open_at = schedule_map["protests_open"]
            round_obj.protests_close_at = schedule_map["protests_close"]
            session.add(round_obj)
            await session.flush()
            from cogs.communication import build_round_schedule_messages

            for schedule in build_round_schedule_messages(guild_record, round_obj):
                from database.models import ScheduledMessage

                session.add(
                    ScheduledMessage(
                        guild_id=interaction.guild.id,
                        round_id=round_obj.id,
                        type=schedule["type"],
                        channel_purpose=schedule["channel_purpose"],
                        scheduled_for=schedule["scheduled_for"],
                    )
                )
            await session.commit()
        await interaction.response.edit_message(embed=round_created_embed(state), view=None)

    async def _fetch_points_systems(self, guild_id: int) -> list[dict[str, object]]:
        async with SessionFactory() as session:
            result = await session.execute(select(PointsSystem).where(PointsSystem.guild_id == guild_id))
            points_systems = result.scalars().all()
        return [
            {
                "id": system.id,
                "name": system.name,
                "description": ", ".join(str(value) for value in system.points_per_position[:5]),
            }
            for system in points_systems
        ]


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminCog(bot))
