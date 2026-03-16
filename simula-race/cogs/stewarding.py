from __future__ import annotations

from collections import Counter
from datetime import timedelta
from math import ceil

import discord
from discord import app_commands
from discord.ext import commands
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from database.engine import SessionFactory
from database.models import ChannelConfig, ChannelPurpose, Driver, Guild, PenaltyPoint, PenaltyPointType, Protest, ProtestStatus, RaceResult, Round, RoundStatus, Season, StaffMember, StaffRole
from utils.embeds import make_embed, make_error_embed, make_success_embed, make_warning_embed
from utils.permissions import resolve_staff_roles
from utils.strings import S
from utils.time_utils import ensure_timezone, format_date_time, now_tz
from utils.validators import validate_required_url
from views.protest_views import AppealModal, AppealView, PenaltySelectView, ProtestPayload, ProtestWizardView, StewardVotingView


async def can_steward_vote(steward_id: int, protest: Protest, guild_id: int) -> bool:
    async with SessionFactory() as session:
        result = await session.execute(
            select(Driver).where(Driver.guild_id == guild_id, Driver.discord_id == steward_id)
        )
        author = result.scalar_one_or_none()
        if author and (author.id == protest.author_driver_id or author.id == protest.accused_driver_id):
            return False
        return True


def vote_majority_threshold(total_stewards: int) -> int:
    return max(2, ceil(total_stewards / 2))


class SimpleReasoningModal(discord.ui.Modal):
    def __init__(self, verdict: str, callback) -> None:
        super().__init__(title=S.STEWARD_REASONING_TITLE)
        self.verdict = verdict
        self.callback_handler = callback
        self.reasoning = discord.ui.TextInput(
            label=S.STEWARD_REASONING_TITLE,
            placeholder=S.STEWARD_REASONING_PLACEHOLDER,
            style=discord.TextStyle.paragraph,
            max_length=500,
        )
        self.add_item(self.reasoning)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.callback_handler(interaction, self.verdict, str(self.reasoning.value))


class StewardingCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def _get_latest_protest_round(self, guild_id: int) -> tuple[Guild, Round] | None:
        async with SessionFactory() as session:
            result = await session.execute(
                select(Guild, Round)
                .join(Season, Season.guild_id == Guild.id)
                .join(Round, Round.season_id == Season.id)
                .where(Guild.id == guild_id)
                .order_by(Round.date_time.desc())
            )
            return result.first()

    @app_commands.command(name="protesto", description=S.CMD_PROTEST)
    async def protest(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            return
        latest = await self._get_latest_protest_round(interaction.guild.id)
        if latest is None:
            await interaction.response.send_message(S.NO_COMPLETED_ROUND, ephemeral=True)
            return
        guild_record, round_obj = latest
        current_time = now_tz(guild_record.timezone)
        if round_obj.status == RoundStatus.SCHEDULED:
            await interaction.response.send_message(S.NO_COMPLETED_ROUND, ephemeral=True)
            return
        if round_obj.protests_open_at and current_time < ensure_timezone(round_obj.protests_open_at, guild_record.timezone):
            _, open_time = format_date_time(round_obj.protests_open_at, guild_record.timezone)
            await interaction.response.send_message(
                S.PROTEST_COOLDOWN.format(n=round_obj.round_number, open_time=open_time),
                ephemeral=True,
            )
            return
        if round_obj.protests_close_at and current_time > ensure_timezone(round_obj.protests_close_at, guild_record.timezone):
            _, close_time = format_date_time(round_obj.protests_close_at, guild_record.timezone)
            await interaction.response.send_message(
                S.PROTEST_EXPIRED.format(n=round_obj.round_number, close_time=close_time),
                ephemeral=True,
            )
            return
        async with SessionFactory() as session:
            author_result = await session.execute(
                select(Driver).where(Driver.guild_id == interaction.guild.id, Driver.discord_id == interaction.user.id)
            )
            author = author_result.scalar_one_or_none()
            if author is None:
                await interaction.response.send_message(S.PROTEST_NOT_PARTICIPANT, ephemeral=True)
                return
            result_rows = await session.execute(
                select(RaceResult, Driver)
                .join(Driver, Driver.id == RaceResult.driver_id)
                .where(RaceResult.round_id == round_obj.id)
            )
            participants = result_rows.all()
            participant_ids = {driver.id for _, driver in participants}
            if author.id not in participant_ids:
                await interaction.response.send_message(S.PROTEST_NOT_PARTICIPANT, ephemeral=True)
                return
            accused_options = [
                (driver.id, f"{driver.real_name or driver.discord_name} (#{driver.car_number or '-'})")
                for _, driver in participants
                if driver.id != author.id
            ]
            view = ProtestWizardView(interaction.user.id, round_obj.round_number, accused_options, self.submit_protest)
            await interaction.response.send_message(embed=make_embed(S.PROTEST_BTN), view=view, ephemeral=True)

    async def submit_protest(self, interaction: discord.Interaction, payload: ProtestPayload) -> None:
        if interaction.guild is None:
            return
        async with SessionFactory() as session:
            guild_result = await session.execute(select(Guild).where(Guild.id == interaction.guild.id))
            guild_record = guild_result.scalar_one()
            round_result = await session.execute(
                select(Round)
                .join(Round.season)
                .where(Season.guild_id == interaction.guild.id)
                .order_by(Round.date_time.desc())
            )
            round_obj = round_result.scalars().first()
            if round_obj is None:
                await interaction.response.send_message(S.NO_COMPLETED_ROUND, ephemeral=True)
                return
            author_result = await session.execute(
                select(Driver).where(Driver.guild_id == interaction.guild.id, Driver.discord_id == interaction.user.id)
            )
            author = author_result.scalar_one()
            protest = Protest(
                guild_id=interaction.guild.id,
                round_id=round_obj.id,
                author_driver_id=author.id,
                accused_driver_id=payload.accused_driver_id,
                lap_number=payload.lap_number,
                turn_zone=payload.turn_zone,
                description=payload.description,
                evidence_url=validate_required_url(payload.evidence_url),
                cooldown_expires_at=round_obj.protests_open_at,
            )
            session.add(protest)
            await session.flush()
            channel_result = await session.execute(
                select(ChannelConfig).where(ChannelConfig.guild_id == interaction.guild.id, ChannelConfig.purpose == ChannelPurpose.STEWARD_DELIBERATION)
            )
            channel_cfg = channel_result.scalar_one_or_none()
            if channel_cfg is not None:
                channel = interaction.guild.get_channel(channel_cfg.channel_id)
                if isinstance(channel, discord.TextChannel):
                    embed = make_embed(
                        S.STEWARD_NEW_PROTEST.format(
                            id=protest.id,
                            author=author.real_name or author.discord_name,
                            accused=payload.accused_label,
                            n=round_obj.round_number,
                            lap=payload.lap_number,
                            zone=payload.turn_zone,
                            description=payload.description,
                            evidence=payload.evidence_url,
                        )
                    )
                    message = await channel.send(embed=embed, view=StewardVotingView())
                    protest.staff_message_id = message.id
            await session.commit()
            await interaction.response.edit_message(
                embed=make_success_embed(
                    S.PROTEST_SUCCESS.format(
                        id=protest.id,
                        accused=payload.accused_label,
                        n=round_obj.round_number,
                        lap=payload.lap_number,
                        zone=payload.turn_zone,
                    )
                ),
                view=None,
            )

    async def handle_steward_action(self, interaction: discord.Interaction, action: str) -> None:
        if interaction.guild is None or interaction.message is None:
            return
        async with SessionFactory() as session:
            result = await session.execute(
                select(Protest)
                .options(selectinload(Protest.author_driver), selectinload(Protest.accused_driver), selectinload(Protest.round).selectinload(Round.season))
                .where(Protest.staff_message_id == interaction.message.id)
            )
            protest = result.scalars().first()
            if protest is None:
                return
            roles = await resolve_staff_roles(SessionFactory, interaction.guild.id, interaction.user.id, interaction.guild.owner_id)
            if not roles.intersection({"owner", "admin", "steward"}):
                await interaction.response.send_message(S.NO_PERMISSION, ephemeral=True)
                return
            if not await can_steward_vote(interaction.user.id, protest, interaction.guild.id):
                await interaction.response.send_message(S.STEWARD_CONFLICT, ephemeral=True)
                return
            if action == "claim":
                protest.status = ProtestStatus.CLAIMED
                if interaction.user.id not in protest.assigned_stewards:
                    protest.assigned_stewards = [*protest.assigned_stewards, interaction.user.id]
                await session.commit()
                await interaction.response.send_message(
                    S.STEWARD_CLAIMED.format(steward=interaction.user.display_name, id=protest.id),
                    ephemeral=True,
                )
                return
            if action == "guilty":
                view = PenaltySelectView(interaction.user.id, lambda i, penalty, pp, reasoning: self.record_penalty_vote(i, protest.id, penalty, pp, reasoning))
                await interaction.response.send_message(S.STEWARD_PENALTY_TITLE, view=view, ephemeral=True)
                return
            await interaction.response.send_modal(
                SimpleReasoningModal(action, lambda i, verdict, reasoning: self.record_simple_vote(i, protest.id, verdict, reasoning))
            )

    async def record_simple_vote(self, interaction: discord.Interaction, protest_id: int, verdict: str, reasoning: str) -> None:
        mapping = {
            "not_guilty": S.STEWARD_VERDICT_NOT_GUILTY,
            "racing_incident": S.STEWARD_VERDICT_RACING_INCIDENT,
            "dismiss": S.STEWARD_VERDICT_DISMISSED,
        }
        await self._record_vote(
            interaction,
            protest_id,
            verdict=mapping[verdict],
            penalty_type=None,
            penalty_value=None,
            penalty_points=0,
            reasoning=reasoning,
        )

    async def record_penalty_vote(self, interaction: discord.Interaction, protest_id: int, penalty: str, pp: int, reasoning: str) -> None:
        await self._record_vote(
            interaction,
            protest_id,
            verdict=S.STEWARD_VERDICT_GUILTY,
            penalty_type=penalty,
            penalty_value=penalty,
            penalty_points=pp,
            reasoning=reasoning,
        )

    async def _record_vote(
        self,
        interaction: discord.Interaction,
        protest_id: int,
        verdict: str,
        penalty_type: str | None,
        penalty_value: str | None,
        penalty_points: int,
        reasoning: str,
    ) -> None:
        async with SessionFactory() as session:
            result = await session.execute(
                select(Protest)
                .options(selectinload(Protest.round).selectinload(Round.season), selectinload(Protest.author_driver), selectinload(Protest.accused_driver))
                .where(Protest.id == protest_id)
            )
            protest = result.scalar_one()
            updated_votes = [vote for vote in protest.votes if int(vote["steward_id"]) != interaction.user.id]
            updated_votes.append(
                {
                    "steward_id": interaction.user.id,
                    "steward_name": interaction.user.display_name,
                    "verdict": verdict,
                    "penalty_type": penalty_type,
                    "penalty_value": penalty_value,
                    "pp": penalty_points,
                    "reasoning": reasoning,
                }
            )
            protest.votes = updated_votes
            if interaction.user.id not in protest.assigned_stewards:
                protest.assigned_stewards = [*protest.assigned_stewards, interaction.user.id]
            total_stewards = await self._count_active_stewards(session, interaction.guild.id)
            counts = Counter(vote["verdict"] for vote in updated_votes)
            top_verdict, top_count = counts.most_common(1)[0]
            threshold = vote_majority_threshold(total_stewards)
            if top_count >= threshold:
                await self._finalize_protest(session, interaction.guild, protest, top_verdict, threshold)
            await session.commit()
        if interaction.response.is_done():
            await interaction.followup.send(S.SUCCESS, ephemeral=True)
        else:
            await interaction.response.send_message(S.SUCCESS, ephemeral=True)

    async def _count_active_stewards(self, session, guild_id: int) -> int:
        result = await session.execute(
            select(func.count(StaffMember.id))
            .where(
                StaffMember.guild_id == guild_id,
                StaffMember.role == StaffRole.STEWARD,
                StaffMember.is_active.is_(True),
            )
        )
        count = int(result.scalar_one() or 0)
        return max(3, count)

    async def _finalize_protest(self, session, guild: discord.Guild, protest: Protest, final_verdict: str, threshold: int) -> None:
        winning_votes = [vote for vote in protest.votes if vote["verdict"] == final_verdict]
        decisive_vote = winning_votes[0]
        protest.status = ProtestStatus.DECIDED
        protest.verdict = final_verdict
        protest.penalty_type = decisive_vote["penalty_type"]
        protest.penalty_value = decisive_vote["penalty_value"]
        protest.penalty_points = int(decisive_vote["pp"])
        protest.reasoning = decisive_vote["reasoning"]
        protest.decided_at = now_tz("Europe/Lisbon")
        protest.appeal_deadline = protest.decided_at + timedelta(hours=24)
        total_pp = 0
        if protest.penalty_points:
            session.add(
                PenaltyPoint(
                    driver_id=protest.accused_driver_id,
                    season_id=protest.round.season.id,
                    protest_id=protest.id,
                    round_id=protest.round.id,
                    points=protest.penalty_points,
                    reason=protest.reasoning or final_verdict,
                    type=PenaltyPointType.PENALTY,
                )
            )
            await session.flush()
            if protest.penalty_value in {"+5s", "+10s", "+30s"}:
                result_row = await session.execute(
                    select(RaceResult).where(RaceResult.round_id == protest.round.id, RaceResult.driver_id == protest.accused_driver_id)
                )
                race_result = result_row.scalar_one_or_none()
                if race_result is not None:
                    race_result.penalty_time_sec += int(str(protest.penalty_value).replace("+", "").replace("s", ""))
            total_pp_result = await session.execute(
                select(func.coalesce(func.sum(PenaltyPoint.points), 0)).where(
                    PenaltyPoint.driver_id == protest.accused_driver_id,
                    PenaltyPoint.season_id == protest.round.season.id,
                )
            )
            total_pp = int(total_pp_result.scalar_one() or 0)
        channel_result = await session.execute(
            select(ChannelConfig).where(ChannelConfig.guild_id == guild.id, ChannelConfig.purpose == ChannelPurpose.STEWARD_DECISIONS)
        )
        channel_cfg = channel_result.scalar_one_or_none()
        if channel_cfg is not None:
            channel = guild.get_channel(channel_cfg.channel_id)
            if isinstance(channel, discord.TextChannel):
                embed = make_embed(
                    S.STEWARD_DECISION_PUBLISHED.format(
                        id=protest.id,
                        author=protest.author_driver.real_name or protest.author_driver.discord_name,
                        accused=protest.accused_driver.real_name or protest.accused_driver.discord_name,
                        n=protest.round.round_number,
                        lap=protest.lap_number,
                        zone=protest.turn_zone,
                        description=protest.description,
                        verdict=protest.verdict,
                        penalty=protest.penalty_value or "-",
                        pp=protest.penalty_points,
                        total_pp=total_pp,
                        max_pp=20,
                        reasoning=protest.reasoning,
                        stewards=", ".join(vote["steward_name"] for vote in winning_votes[:threshold]),
                    )
                )
                message = await channel.send(embed=embed, view=AppealView())
                protest.public_message_id = message.id

    async def handle_appeal_button(self, interaction: discord.Interaction) -> None:
        if interaction.message is None:
            return
        async with SessionFactory() as session:
            result = await session.execute(select(Protest).where(Protest.public_message_id == interaction.message.id))
            protest = result.scalars().first()
            if protest is None:
                return
            if protest.appeal_deadline is None or now_tz("Europe/Lisbon") > ensure_timezone(protest.appeal_deadline):
                await interaction.response.send_message(S.APPEAL_EXPIRED, ephemeral=True)
                return
            await interaction.response.send_modal(AppealModal(protest.id, lambda i, reason: self.submit_appeal(i, protest.id, reason)))

    async def submit_appeal(self, interaction: discord.Interaction, protest_id: int, reason: str) -> None:
        async with SessionFactory() as session:
            result = await session.execute(select(Protest).where(Protest.id == protest_id))
            protest = result.scalar_one()
            protest.appeal_reason = reason
            protest.status = ProtestStatus.APPEALED
            await session.commit()
        await interaction.response.send_message(S.APPEAL_SUCCESS.format(id=protest_id), ephemeral=True)

    @app_commands.command(name="pp", description=S.CMD_PP)
    async def penalty_points(self, interaction: discord.Interaction, piloto: discord.Member | None = None) -> None:
        if interaction.guild is None:
            return
        target = piloto or interaction.user
        async with SessionFactory() as session:
            driver_result = await session.execute(select(Driver).where(Driver.guild_id == interaction.guild.id, Driver.discord_id == target.id))
            driver = driver_result.scalar_one_or_none()
            if driver is None:
                await interaction.response.send_message(S.NOT_REGISTERED, ephemeral=True)
                return
            total_result = await session.execute(
                select(func.coalesce(func.sum(PenaltyPoint.points), 0)).where(PenaltyPoint.driver_id == driver.id)
            )
            history_result = await session.execute(
                select(PenaltyPoint).where(PenaltyPoint.driver_id == driver.id).order_by(PenaltyPoint.created_at.desc()).limit(5)
            )
            total = int(total_result.scalar_one() or 0)
            if total >= 15:
                status = S.PP_STATUS_DANGER
            elif total >= 5:
                status = S.PP_STATUS_WARNING
            else:
                status = S.PP_STATUS_CLEAN
            history = "\n".join(f"• {entry.points:+d} — {entry.reason}" for entry in history_result.scalars().all()) or "-"
            await interaction.response.send_message(
                embed=make_embed(
                    S.PP_STATUS.format(name=target.display_name, total=total, max=20, status=status, history=history)
                ),
                ephemeral=True,
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StewardingCog(bot))
