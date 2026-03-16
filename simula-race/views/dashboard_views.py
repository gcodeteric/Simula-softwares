from __future__ import annotations

from collections.abc import Awaitable, Callable

import discord

from utils.strings import S
from views.common import BaseView


DashboardCallback = Callable[[discord.Interaction, str], Awaitable[None]]


class DashboardView(BaseView):
    def __init__(self, author_id: int, is_staff: bool, callback: DashboardCallback) -> None:
        super().__init__(author_id=author_id, timeout=300)
        self.callback = callback
        self._add_action(S.DASHBOARD_BTN_STANDINGS, "standings", discord.ButtonStyle.primary)
        self._add_action(S.DASHBOARD_BTN_RESULTS, "results", discord.ButtonStyle.primary)
        self._add_action(S.DASHBOARD_BTN_ENTRYLIST, "entrylist", discord.ButtonStyle.primary)
        self._add_action(S.DASHBOARD_BTN_CALENDAR, "calendar", discord.ButtonStyle.primary)
        self._add_action(S.DASHBOARD_BTN_PROTESTS, "protests", discord.ButtonStyle.secondary)
        self._add_action(S.DASHBOARD_BTN_HELP, "help", discord.ButtonStyle.secondary)
        if is_staff:
            self._add_action(S.DASHBOARD_BTN_CONFIG, "config", discord.ButtonStyle.secondary)
            self._add_action(S.DASHBOARD_BTN_NEW_SEASON, "new_season", discord.ButtonStyle.success)
            self._add_action(S.DASHBOARD_BTN_MANAGE_SEASON, "manage_season", discord.ButtonStyle.success)
            self._add_action(S.DASHBOARD_BTN_ADD_ROUND, "add_round", discord.ButtonStyle.success)
            self._add_action(S.DASHBOARD_BTN_MANAGE_STAFF, "manage_staff", discord.ButtonStyle.success)
            self._add_action(S.DASHBOARD_BTN_EXPORT, "export", discord.ButtonStyle.secondary)

    def _add_action(self, label: str, action: str, style: discord.ButtonStyle) -> None:
        button = discord.ui.Button(label=label, style=style)
        button.callback = self._make_callback(action)
        self.add_item(button)

    def _make_callback(self, action: str):
        async def callback(interaction: discord.Interaction) -> None:
            await self.callback(interaction, action)

        return callback
