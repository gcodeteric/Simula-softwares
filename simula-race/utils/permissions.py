from __future__ import annotations

from collections.abc import Sequence

import discord
from discord import app_commands
from sqlalchemy import select

from database.engine import SessionFactory
from database.models import StaffMember
from utils.strings import S


STAFF_ROLE_KEYS = {"admin", "race_director", "steward", "broadcaster"}


async def resolve_staff_roles(
    session_factory: SessionFactory,
    guild_id: int,
    discord_id: int,
    guild_owner_id: int | None = None,
) -> set[str]:
    roles: set[str] = set()
    if guild_owner_id and discord_id == guild_owner_id:
        roles.add("owner")
    async with session_factory() as session:
        result = await session.execute(
            select(StaffMember.role).where(
                StaffMember.guild_id == guild_id,
                StaffMember.discord_id == discord_id,
                StaffMember.is_active.is_(True),
            )
        )
        roles.update(result.scalars().all())
    return roles


async def member_has_permission(
    session_factory: SessionFactory,
    member: discord.abc.User | discord.Member,
    guild: discord.Guild,
    required_roles: Sequence[str] | None = None,
) -> bool:
    roles = await resolve_staff_roles(session_factory, guild.id, member.id, guild.owner_id)
    if required_roles is None:
        return bool(roles & (STAFF_ROLE_KEYS | {"owner"}))
    return bool(roles.intersection(required_roles))


def staff_only(required_roles: Sequence[str] | None = None):
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.guild is None:
            raise app_commands.CheckFailure(S.NO_PERMISSION)
        allowed = await member_has_permission(
            SessionFactory,
            interaction.user,
            interaction.guild,
            required_roles,
        )
        if not allowed:
            raise app_commands.CheckFailure(S.NO_PERMISSION)
        return True

    return app_commands.check(predicate)
