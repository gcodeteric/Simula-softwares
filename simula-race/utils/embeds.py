from __future__ import annotations

import discord

from utils.strings import S


def color_from_hex(value: str) -> int:
    return int(value.replace("#", ""), 16)


def make_embed(description: str, title: str | None = None, color: int = 0xFF6600) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=S.BOT_NAME)
    return embed


def make_success_embed(description: str) -> discord.Embed:
    return make_embed(description=description, title=S.SUCCESS, color=0x2ECC71)


def make_error_embed(description: str) -> discord.Embed:
    return make_embed(description=description, title=S.ERROR, color=0xE74C3C)


def make_warning_embed(description: str) -> discord.Embed:
    return make_embed(description=description, title=S.WARNING, color=0xF1C40F)


def make_dashboard_embed(
    league_name: str,
    season_name: str | None,
    next_round_line: str | None,
    drivers_line: str,
    protests_line: str,
    alerts_line: str,
) -> discord.Embed:
    embed = make_embed(
        description=S.DASHBOARD_SEASON_ACTIVE.format(season_name=season_name)
        if season_name
        else S.DASHBOARD_NO_SEASON,
        title=S.DASHBOARD_TITLE.format(league_name=league_name),
        color=0xFF6600,
    )
    if next_round_line:
        embed.add_field(name=S.DASHBOARD_BTN_CALENDAR, value=next_round_line, inline=False)
    embed.add_field(name=S.DASHBOARD_FIELD_STATUS, value=drivers_line, inline=False)
    embed.add_field(name=S.DASHBOARD_BTN_PROTESTS, value=protests_line, inline=False)
    embed.add_field(name=S.DASHBOARD_ALERTS, value=alerts_line, inline=False)
    return embed
