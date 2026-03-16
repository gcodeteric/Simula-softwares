from __future__ import annotations

import discord

from utils.strings import S


class PersistentRSVPView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    async def _dispatch(self, interaction: discord.Interaction, status: str) -> None:
        cog = interaction.client.get_cog("CommunicationCog")
        if cog is None:
            return
        await cog.handle_rsvp(interaction, status)

    @discord.ui.button(label=S.RSVP_BTN_YES, style=discord.ButtonStyle.success, custom_id="rsvp_yes")
    async def rsvp_yes(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self._dispatch(interaction, "confirmed")

    @discord.ui.button(label=S.RSVP_BTN_MAYBE, style=discord.ButtonStyle.secondary, custom_id="rsvp_maybe")
    async def rsvp_maybe(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self._dispatch(interaction, "maybe")

    @discord.ui.button(label=S.RSVP_BTN_NO, style=discord.ButtonStyle.danger, custom_id="rsvp_no")
    async def rsvp_no(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self._dispatch(interaction, "absent")
