from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands
from sqlalchemy import case, func, select
from sqlalchemy.orm import selectinload

from database.engine import SessionFactory
from database.models import ChannelConfig, ChannelPurpose, Division, Driver, Registration, RegistrationStatus, Season, SeasonStatus
from utils.embeds import make_embed, make_error_embed, make_success_embed
from utils.strings import S
from utils.time_utils import format_date_time
from utils.validators import parse_hotlap_to_ms, validate_car_number, validate_non_empty
from views.registration_views import ApprovalView, RegistrationEntryView, RegistrationPayload


async def get_registration_season(guild_id: int) -> Season | None:
    async with SessionFactory() as session:
        result = await session.execute(
            select(Season)
            .options(selectinload(Season.divisions))
            .where(Season.guild_id == guild_id, Season.status.in_([SeasonStatus.REGISTRATION, SeasonStatus.ACTIVE]))
            .order_by(
                case((Season.status == SeasonStatus.ACTIVE, 0), else_=1),
                Season.created_at.desc(),
                Season.id.desc(),
            )
        )
        return result.scalars().first()


class RegistrationCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="inscrever", description=S.CMD_REGISTER)
    async def register(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            return
        season = await get_registration_season(interaction.guild.id)
        if season is None:
            await interaction.response.send_message(S.REGISTER_CLOSED, ephemeral=True)
            return
        view = RegistrationEntryView(interaction.user.id, season.name, self.submit_registration)
        await interaction.response.send_message(embed=make_embed(S.REGISTER_TITLE), view=view, ephemeral=True)

    async def submit_registration(self, interaction: discord.Interaction, payload: RegistrationPayload) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            season_result = await session.execute(
                select(Season)
                .options(selectinload(Season.divisions))
                .where(Season.guild_id == interaction.guild.id, Season.status.in_([SeasonStatus.REGISTRATION, SeasonStatus.ACTIVE]))
                .order_by(
                    case((Season.status == SeasonStatus.ACTIVE, 0), else_=1),
                    Season.created_at.desc(),
                    Season.id.desc(),
                )
            )
            season = season_result.scalars().first()
            if season is None:
                await interaction.response.send_message(S.REGISTER_CLOSED, ephemeral=True)
                return
            if payload.car_number:
                payload.car_number = validate_car_number(payload.car_number)
            driver_result = await session.execute(
                select(Driver).where(Driver.guild_id == interaction.guild.id, Driver.discord_id == interaction.user.id)
            )
            driver = driver_result.scalar_one_or_none()
            if driver is None:
                driver = Driver(
                    guild_id=interaction.guild.id,
                    discord_id=interaction.user.id,
                    discord_name=interaction.user.display_name,
                    real_name=payload.real_name,
                    steam_id=payload.game_id,
                    nationality=payload.nationality,
                    car_number=payload.car_number,
                    team_name=payload.team_name,
                )
                session.add(driver)
                await session.flush()
            registration_result = await session.execute(
                select(Registration).where(Registration.driver_id == driver.id, Registration.season_id == season.id)
            )
            existing = registration_result.scalar_one_or_none()
            if existing and existing.status != RegistrationStatus.WITHDRAWN:
                await interaction.response.send_message(S.REGISTER_ALREADY, ephemeral=True)
                return
            division = season.divisions[0] if season.divisions else None
            registration = existing or Registration(driver_id=driver.id, season_id=season.id, division_id=division.id if division else None)
            registration.status = RegistrationStatus.PENDING
            registration.rejection_reason = None
            session.add(registration)
            await session.commit()
            await interaction.response.send_message(
                embed=make_success_embed(
                    S.REGISTER_SUCCESS.format(name=interaction.user.display_name)
                ),
                ephemeral=True,
            )
            await self._notify_staff(session, interaction.guild, registration.id, payload, season.name)

    async def _notify_staff(self, session, guild: discord.Guild, registration_id: int, payload: RegistrationPayload, season_name: str) -> None:
        channel_result = await session.execute(
            select(ChannelConfig).where(ChannelConfig.guild_id == guild.id, ChannelConfig.purpose == ChannelPurpose.STAFF_GENERAL)
        )
        channel_cfg = channel_result.scalar_one_or_none()
        if channel_cfg is None:
            return
        channel = guild.get_channel(channel_cfg.channel_id)
        if not isinstance(channel, discord.TextChannel):
            return
        embed = make_embed(
            S.APPROVE_NOTIFICATION.format(
                name=payload.real_name or "-",
                game_id=payload.game_id,
                car_number=payload.car_number,
                nationality=payload.nationality or "-",
            ),
            title=season_name,
        )
        view = ApprovalView(registration_id, self.approve_registration, self.reject_registration, self.show_profile)
        await channel.send(embed=embed, view=view)

    async def approve_registration(self, interaction: discord.Interaction, registration_id: int, _: str) -> None:
        async with SessionFactory() as session:
            result = await session.execute(
                select(Registration)
                .options(selectinload(Registration.driver), selectinload(Registration.season), selectinload(Registration.division))
                .where(Registration.id == registration_id)
            )
            registration = result.scalar_one()
            registration.status = RegistrationStatus.APPROVED
            registration.approved_by = interaction.user.id
            await session.commit()
            if interaction.response.is_done():
                await interaction.followup.send(embed=make_success_embed(S.SUCCESS), ephemeral=True)
            else:
                await interaction.response.edit_message(view=None)
            user = self.bot.get_user(registration.driver.discord_id)
            if user is not None:
                try:
                    await user.send(
                        S.APPROVED_DM.format(
                            season_name=registration.season.name,
                            division=registration.division.name if registration.division else S.DEFAULT_DIVISION_NAME,
                            car_number=registration.driver.car_number or 0,
                        )
                    )
                except discord.Forbidden:
                    return

    async def reject_registration(self, interaction: discord.Interaction, registration_id: int, reason: str) -> None:
        async with SessionFactory() as session:
            result = await session.execute(
                select(Registration)
                .options(selectinload(Registration.driver), selectinload(Registration.season))
                .where(Registration.id == registration_id)
            )
            registration = result.scalar_one()
            registration.status = RegistrationStatus.REJECTED
            registration.rejection_reason = validate_non_empty(reason)
            await session.commit()
            await interaction.response.edit_message(view=None)
            user = self.bot.get_user(registration.driver.discord_id)
            if user is not None:
                try:
                    await user.send(S.REJECTED_DM.format(reason=registration.rejection_reason))
                except discord.Forbidden:
                    return

    async def show_profile(self, interaction: discord.Interaction, registration_id: int) -> None:
        async with SessionFactory() as session:
            result = await session.execute(
                select(Registration)
                .options(selectinload(Registration.driver))
                .where(Registration.id == registration_id)
            )
            registration = result.scalar_one()
            embed = make_embed(
                S.PROFILE_SUMMARY.format(
                    discord_name=registration.driver.discord_name,
                    game_id=registration.driver.steam_id or registration.driver.iracing_id or "-",
                    car_number=registration.driver.car_number or "-",
                    team_name=registration.driver.team_name or "-",
                )
            )
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="desistir", description=S.CMD_WITHDRAW)
    async def withdraw(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            result = await session.execute(
                select(Registration)
                .join(Registration.driver)
                .join(Registration.season)
                .where(
                    Driver.discord_id == interaction.user.id,
                    Driver.guild_id == interaction.guild.id,
                    Season.guild_id == interaction.guild.id,
                )
                .order_by(Registration.registered_at.desc())
            )
            registration = result.scalars().first()
            if registration is None:
                await interaction.response.send_message(S.NOT_REGISTERED, ephemeral=True)
                return
            registration.status = RegistrationStatus.WITHDRAWN
            await session.commit()
            await interaction.response.send_message(S.REGISTER_WITHDRAWN, ephemeral=True)

    @app_commands.command(name="entrylist", description=S.CMD_ENTRYLIST)
    async def entrylist(self, interaction: discord.Interaction) -> None:
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
            registrations_result = await session.execute(
                select(Registration)
                .options(selectinload(Registration.driver))
                .where(Registration.season_id == season.id)
                .order_by(Registration.id.asc())
            )
            registrations = registrations_result.scalars().all()
            rows = [
                S.ENTRYLIST_ROW.format(
                    number=registration.driver.car_number or 0,
                    flag=registration.driver.nationality_flag or "🏳️",
                    name=registration.driver.real_name or registration.driver.discord_name,
                    team=registration.driver.team_name or "-",
                )
                for registration in registrations
            ]
            approved = sum(1 for registration in registrations if registration.status == RegistrationStatus.APPROVED)
            pending = sum(1 for registration in registrations if registration.status == RegistrationStatus.PENDING)
            embed = make_embed("\n".join(rows) or "-", title=S.ENTRYLIST_TITLE.format(season_name=season.name))
            embed.set_footer(text=S.ENTRYLIST_FOOTER.format(total=len(registrations), approved=approved, pending=pending))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="hotlap", description=S.CMD_HOTLAP)
    async def hotlap(self, interaction: discord.Interaction, tempo: str) -> None:
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
            registration_result = await session.execute(
                select(Registration)
                .join(Registration.driver)
                .where(
                    Driver.guild_id == interaction.guild.id,
                    Driver.discord_id == interaction.user.id,
                    Registration.season_id == season.id,
                )
            )
            registration = registration_result.scalar_one_or_none()
            if registration is None:
                await interaction.response.send_message(S.NOT_REGISTERED, ephemeral=True)
                return
            registration.hotlap_time_ms = parse_hotlap_to_ms(tempo)
            registration.hotlap_track = "-"
            await session.commit()
            await interaction.response.send_message(S.HOTLAP_RECORDED, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RegistrationCog(bot))
