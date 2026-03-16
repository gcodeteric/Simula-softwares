from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import discord
from discord import app_commands
from discord.ext import commands
from sqlalchemy import Select, func, select
from sqlalchemy.orm import selectinload

from config import DATA_DIR, get_settings
from database.engine import SessionFactory
from database.models import ChannelConfig, ChannelPurpose, Driver, Guild, Protest, Round, RSVP, RSVPStatus, ScheduledMessage, ScheduledMessageType, Season
from utils.embeds import make_embed, make_success_embed
from utils.strings import S
from utils.time_utils import calculate_round_schedule, format_date_time
from views.rsvp_views import PersistentRSVPView


LOGGER = logging.getLogger(__name__)


def build_round_schedule_messages(guild: Guild, round_obj: Round) -> list[dict[str, Any]]:
    schedule = calculate_round_schedule(round_obj.date_time, guild.cooldown_hours, guild.protest_deadline_h)
    return [
        {"type": ScheduledMessageType.ANNOUNCEMENT, "channel_purpose": ChannelPurpose.ANNOUNCEMENTS, "scheduled_for": schedule["announcement"]},
        {"type": ScheduledMessageType.BRIEFING, "channel_purpose": ChannelPurpose.BRIEFING, "scheduled_for": schedule["briefing"]},
        {"type": ScheduledMessageType.REMINDER_DAY, "channel_purpose": ChannelPurpose.ANNOUNCEMENTS, "scheduled_for": schedule["reminder_day"]},
        {"type": ScheduledMessageType.REMINDER_FINAL, "channel_purpose": ChannelPurpose.ANNOUNCEMENTS, "scheduled_for": schedule["reminder_final"]},
        {"type": ScheduledMessageType.PROTESTS_OPEN, "channel_purpose": ChannelPurpose.PROTESTS, "scheduled_for": schedule["protests_open"]},
        {"type": ScheduledMessageType.PROTESTS_CLOSE, "channel_purpose": ChannelPurpose.PROTESTS, "scheduled_for": schedule["protests_close"]},
    ]


def build_rsvp_counts_embed(round_obj: Round, counts: dict[str, int]) -> discord.Embed:
    date_value, time_value = format_date_time(round_obj.date_time, round_obj.season.guild.timezone)
    description = (
        f"{S.RSVP_TITLE.format(n=round_obj.round_number, track=round_obj.track_name, date=date_value, time=time_value)}\n"
        f"{S.RSVP_COUNT.format(yes=counts['confirmed'], maybe=counts['maybe'], no=counts['absent'])}"
    )
    return make_embed(description, title=S.COMM_ANNOUNCE_D7.format(
        n=round_obj.round_number,
        track=round_obj.track_name,
        flag=round_obj.track_flag or "",
        date=date_value,
        time=time_value,
        weather=round_obj.weather,
        duration=round_obj.race_duration_min,
        format=round_obj.format,
    ))


class CommunicationCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.settings = get_settings()
        self.scheduler = AsyncIOScheduler(timezone=self.settings.timezone)

    async def cog_load(self) -> None:
        if not self.scheduler.running:
            self.scheduler.add_job(self.dispatch_due_messages, "interval", minutes=1, id="dispatch_due_messages", replace_existing=True)
            self.scheduler.start()

    async def cog_unload(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)

    async def dispatch_due_messages(self) -> None:
        async with SessionFactory() as session:
            result = await session.execute(
                select(ScheduledMessage)
                .options(selectinload(ScheduledMessage.round).selectinload(Round.season).selectinload(Season.guild))
                .where(
                    ScheduledMessage.sent.is_(False),
                    ScheduledMessage.scheduled_for <= func.now(),
                )
            )
            messages = result.scalars().all()
            for scheduled in messages:
                if scheduled.round is None:
                    continue
                guild = self.bot.get_guild(scheduled.guild_id)
                if guild is None:
                    continue
                channel = await self._resolve_channel(session, scheduled.guild_id, scheduled.channel_purpose)
                if channel is None:
                    continue
                embed, view = await self._build_message_payload(session, scheduled)
                message = await channel.send(embed=embed, view=view)
                scheduled.sent = True
                scheduled.sent_at = func.now()
                scheduled.message_id = message.id
            await session.commit()

    async def _resolve_channel(self, session, guild_id: int, purpose: ChannelPurpose) -> discord.TextChannel | None:
        result = await session.execute(
            select(ChannelConfig).where(ChannelConfig.guild_id == guild_id, ChannelConfig.purpose == purpose)
        )
        channel_cfg = result.scalar_one_or_none()
        if channel_cfg is None:
            return None
        channel = self.bot.get_channel(channel_cfg.channel_id)
        if isinstance(channel, discord.TextChannel):
            return channel
        return None

    async def _build_message_payload(self, session, scheduled: ScheduledMessage) -> tuple[discord.Embed, discord.ui.View | None]:
        round_obj = scheduled.round
        assert round_obj is not None
        if scheduled.type == ScheduledMessageType.ANNOUNCEMENT:
            counts = await self._count_rsvp(session, round_obj.id)
            return build_rsvp_counts_embed(round_obj, counts), PersistentRSVPView()
        if scheduled.type == ScheduledMessageType.BRIEFING:
            date_value, time_value = format_date_time(round_obj.date_time, round_obj.season.guild.timezone)
            return make_embed(
                S.COMM_BRIEFING.format(
                    n=round_obj.round_number,
                    track=round_obj.track_name,
                    flag=round_obj.track_flag or "",
                    date=date_value,
                    time=time_value,
                    weather=round_obj.weather,
                    duration=round_obj.race_duration_min,
                    start_type=round_obj.start_type,
                    track_limits=round_obj.track_limits_notes or "-",
                    notes=round_obj.briefing_text or "-",
                )
            ), None
        if scheduled.type == ScheduledMessageType.REMINDER_DAY:
            counts = await self._count_rsvp(session, round_obj.id)
            date_value, time_value = format_date_time(round_obj.date_time, round_obj.season.guild.timezone)
            return make_embed(
                S.COMM_REMINDER_D1.format(
                    n=round_obj.round_number,
                    track=round_obj.track_name,
                    date=date_value,
                    time=time_value,
                    rsvp_yes=counts["confirmed"],
                    rsvp_maybe=counts["maybe"],
                )
            ), None
        if scheduled.type == ScheduledMessageType.REMINDER_FINAL:
            counts = await self._count_rsvp(session, round_obj.id)
            _, race_time = format_date_time(round_obj.date_time, round_obj.season.guild.timezone)
            return make_embed(
                S.COMM_REMINDER_H2.format(
                    track=round_obj.track_name,
                    server_open=race_time,
                    race_start=race_time,
                    rsvp_yes=counts["confirmed"],
                )
            ), None
        if scheduled.type == ScheduledMessageType.PROTESTS_OPEN:
            _, close_time = format_date_time(round_obj.protests_close_at or round_obj.date_time, round_obj.season.guild.timezone)
            return make_embed(S.COMM_PROTESTS_OPEN.format(n=round_obj.round_number, close_time=close_time)), None
        count_result = await session.execute(select(func.count(Protest.id)).where(Protest.round_id == round_obj.id))
        protest_count = int(count_result.scalar_one() or 0)
        return make_embed(S.COMM_PROTESTS_CLOSE.format(n=round_obj.round_number, count=protest_count)), None

    async def _count_rsvp(self, session, round_id: int) -> dict[str, int]:
        counts = {"confirmed": 0, "maybe": 0, "absent": 0}
        result = await session.execute(select(RSVP.status, func.count(RSVP.id)).where(RSVP.round_id == round_id).group_by(RSVP.status))
        for status, count in result.all():
            counts[str(status)] = int(count)
        return counts

    async def handle_rsvp(self, interaction: discord.Interaction, status: str) -> None:
        if interaction.guild is None or interaction.message is None:
            return
        async with SessionFactory() as session:
            result = await session.execute(
                select(ScheduledMessage)
                .options(selectinload(ScheduledMessage.round).selectinload(Round.season).selectinload(Season.guild))
                .where(ScheduledMessage.message_id == interaction.message.id)
            )
            scheduled = result.scalars().first()
            if scheduled is None or scheduled.round is None:
                return
            driver_result = await session.execute(
                select(Driver).where(Driver.guild_id == interaction.guild.id, Driver.discord_id == interaction.user.id)
            )
            driver = driver_result.scalar_one_or_none()
            if driver is None:
                await interaction.response.send_message(S.NOT_REGISTERED, ephemeral=True)
                return
            rsvp_result = await session.execute(select(RSVP).where(RSVP.round_id == scheduled.round.id, RSVP.driver_id == driver.id))
            rsvp = rsvp_result.scalar_one_or_none()
            if rsvp is None:
                rsvp = RSVP(round_id=scheduled.round.id, driver_id=driver.id, status=RSVPStatus(status))
                session.add(rsvp)
            else:
                rsvp.status = RSVPStatus(status)
            await session.commit()
            counts = await self._count_rsvp(session, scheduled.round.id)
            embed = build_rsvp_counts_embed(scheduled.round, counts)
            await interaction.response.edit_message(embed=embed, view=PersistentRSVPView())

    @app_commands.command(name="anuncio", description=S.CMD_ANNOUNCE)
    async def announce(self, interaction: discord.Interaction, texto: str) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            channel = await self._resolve_channel(session, interaction.guild.id, ChannelPurpose.ANNOUNCEMENTS)
            if channel is None:
                await interaction.response.send_message(S.ERROR, ephemeral=True)
                return
            await channel.send(embed=make_embed(texto))
            await interaction.response.send_message(embed=make_success_embed(S.SUCCESS), ephemeral=True)

    @app_commands.command(name="briefing", description=S.CMD_BRIEFING)
    async def briefing(self, interaction: discord.Interaction, ronda: int, texto: str | None = None) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            result = await session.execute(
                select(Round)
                .options(selectinload(Round.season).selectinload(Season.guild))
                .join(Round.season)
                .where(Round.round_number == ronda, Round.season.has(guild_id=interaction.guild.id))
                .order_by(Round.date_time.desc())
            )
            round_obj = result.scalars().first()
            if round_obj is None:
                await interaction.response.send_message(S.NO_COMPLETED_ROUND, ephemeral=True)
                return
            channel = await self._resolve_channel(session, interaction.guild.id, ChannelPurpose.BRIEFING)
            if channel is None:
                await interaction.response.send_message(S.ERROR, ephemeral=True)
                return
            date_value, time_value = format_date_time(round_obj.date_time, round_obj.season.guild.timezone)
            await channel.send(
                embed=make_embed(
                    S.COMM_BRIEFING.format(
                        n=round_obj.round_number,
                        track=round_obj.track_name,
                        flag=round_obj.track_flag or "",
                        date=date_value,
                        time=time_value,
                        weather=round_obj.weather,
                        duration=round_obj.race_duration_min,
                        start_type=round_obj.start_type,
                        track_limits=round_obj.track_limits_notes or "-",
                        notes=texto or round_obj.briefing_text or "-",
                    )
                )
            )
            await interaction.response.send_message(embed=make_success_embed(S.SUCCESS), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CommunicationCog(bot))
