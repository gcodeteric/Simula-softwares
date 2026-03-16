from __future__ import annotations

import asyncio

import discord
from discord import app_commands
from discord.ext import commands
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from config import DATA_DIR, get_settings
from database.engine import SessionFactory
from database.models import Driver, Guild, PenaltyPoint, Protest, ProtestStatus, Registration, RegistrationStatus, Round, Season
from generators.image_calendar import generate_calendar_image
from utils.embeds import make_dashboard_embed, make_embed
from utils.permissions import member_has_permission
from utils.strings import S
from utils.time_utils import format_short_date_time
from views.common import BackToDashboardView
from views.dashboard_views import DashboardView


class DashboardCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.settings = get_settings()

    @app_commands.command(name="painel", description=S.CMD_DASHBOARD)
    async def dashboard(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            return
        embed, is_staff = await self._build_dashboard(interaction.guild, interaction.user)
        view = DashboardView(interaction.user.id, is_staff, self.handle_action)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    async def _build_dashboard(self, guild: discord.Guild, user: discord.abc.User | discord.Member) -> tuple[discord.Embed, bool]:
        async with SessionFactory() as session:
            guild_result = await session.execute(select(Guild).where(Guild.id == guild.id))
            guild_record = guild_result.scalars().first()
            season_result = await session.execute(
                select(Season)
                .options(selectinload(Season.rounds))
                .where(Season.guild_id == guild.id)
                .order_by(Season.created_at.desc())
            )
            season = season_result.scalars().first()
            approved_result = await session.execute(
                select(func.count(Registration.id)).join(Registration.season).where(Season.guild_id == guild.id, Registration.status == RegistrationStatus.APPROVED)
            )
            pending_result = await session.execute(
                select(func.count(Protest.id)).join(Protest.round).join(Round.season).where(Season.guild_id == guild.id, Protest.status == ProtestStatus.SUBMITTED)
            )
            total_pp_result = await session.execute(
                select(Driver.discord_name, func.coalesce(func.sum(PenaltyPoint.points), 0).label("pp"))
                .join(PenaltyPoint, PenaltyPoint.driver_id == Driver.id)
                .where(Driver.guild_id == guild.id)
                .group_by(Driver.id)
                .order_by(func.sum(PenaltyPoint.points).desc())
                .limit(1)
            )
            top_alert = total_pp_result.first()
            next_round = None
            if season is not None:
                round_result = await session.execute(
                    select(Round).where(Round.season_id == season.id).order_by(Round.round_number.asc())
                )
                rounds = round_result.scalars().all()
                next_round = next((round_obj for round_obj in rounds if round_obj.status in {"scheduled", "next"}), rounds[-1] if rounds else None)
            next_round_line = None
            if next_round is not None:
                date_value, time_value = format_short_date_time(next_round.date_time, guild_record.timezone if guild_record else "Europe/Lisbon")
                next_round_line = S.DASHBOARD_NEXT_ROUND.format(track=next_round.track_name, date=date_value, time=time_value)
            alerts_line = (
                S.DASHBOARD_PP_ALERT.format(driver=top_alert[0], pp=top_alert[1], max_pp=guild_record.max_penalty_points if guild_record else 20, consequence="suspensão")
                if top_alert and guild_record
                else "-"
            )
            approved_count = int(approved_result.scalar_one() or 0)
            pending_count = int(pending_result.scalar_one() or 0)
            embed = make_dashboard_embed(
                league_name=guild_record.league_name if guild_record else guild.name,
                season_name=season.name if season else None,
                next_round_line=next_round_line,
                drivers_line=S.DASHBOARD_DRIVERS.format(approved=approved_count, active=approved_count),
                protests_line=S.DASHBOARD_PROTESTS.format(pending=pending_count, review=0),
                alerts_line=alerts_line,
            )
            is_staff = await member_has_permission(SessionFactory, user, guild)
            return embed, is_staff

    async def handle_action(self, interaction: discord.Interaction, action: str) -> None:
        if interaction.guild is None:
            return
        if action == "help":
            view = BackToDashboardView(interaction.user.id, self._return_to_dashboard)
            await interaction.response.edit_message(embed=make_embed(S.HELP_MAIN), view=view)
            return
        if action == "new_season":
            admin = self.bot.get_cog("AdminCog")
            if admin is not None:
                await admin.start_season_wizard(interaction)
            return
        if action == "add_round":
            admin = self.bot.get_cog("AdminCog")
            if admin is not None:
                await admin.start_round_wizard(interaction)
            return
        if action == "standings":
            results = self.bot.get_cog("ResultsCog")
            if results is not None:
                await results.standings.callback(results, interaction)
            return
        if action == "results":
            results = self.bot.get_cog("ResultsCog")
            if results is not None:
                await results.results.callback(results, interaction, None)
            return
        if action == "entrylist":
            registration = self.bot.get_cog("RegistrationCog")
            if registration is not None:
                await registration.entrylist.callback(registration, interaction)
            return
        if action == "calendar":
            await self._show_calendar(interaction)
            return
        if action == "protests":
            view = BackToDashboardView(interaction.user.id, self._return_to_dashboard)
            await interaction.response.edit_message(embed=make_embed(S.HELP_PROTESTS, title=S.DASHBOARD_BTN_PROTESTS), view=view)
            return
        view = BackToDashboardView(interaction.user.id, self._return_to_dashboard)
        await interaction.response.edit_message(embed=make_embed(S.GENERIC_HELP, title=action), view=view)

    async def _show_calendar(self, interaction: discord.Interaction) -> None:
        async with SessionFactory() as session:
            season_result = await session.execute(select(Season).where(Season.guild_id == interaction.guild.id).order_by(Season.created_at.desc()))
            season = season_result.scalars().first()
            guild_result = await session.execute(select(Guild).where(Guild.id == interaction.guild.id))
            guild_record = guild_result.scalars().first()
            if season is None or guild_record is None:
                await interaction.response.send_message(S.DASHBOARD_NO_SEASON, ephemeral=True)
                return
            rounds_result = await session.execute(select(Round).where(Round.season_id == season.id).order_by(Round.round_number.asc()))
            rounds = rounds_result.scalars().all()
            rows = []
            for round_obj in rounds:
                date_value, time_value = format_short_date_time(round_obj.date_time, guild_record.timezone)
                rows.append(
                    {
                        "status": "✅" if round_obj.status == "finished" else "🔴" if round_obj.status == "next" else "⬜",
                        "round_number": round_obj.round_number,
                        "track": round_obj.track_name,
                        "flag": round_obj.track_flag or "",
                        "date": date_value,
                        "time": time_value,
                    }
                )
            output = await asyncio.to_thread(
                generate_calendar_image,
                DATA_DIR / f"calendar_season_{season.id}.png",
                rows,
                S.DASHBOARD_BTN_CALENDAR,
                guild_record.primary_color,
                guild_record.secondary_color,
                self.settings.font_path,
                self.settings.font_bold_path,
            )
        await interaction.response.send_message(file=discord.File(output), ephemeral=True)

    async def _return_to_dashboard(self, interaction: discord.Interaction) -> None:
        embed, is_staff = await self._build_dashboard(interaction.guild, interaction.user)
        view = DashboardView(interaction.user.id, is_staff, self.handle_action)
        await interaction.response.edit_message(embed=embed, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DashboardCog(bot))
