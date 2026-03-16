from __future__ import annotations

from collections.abc import Awaitable, Callable

import discord

from utils.embeds import make_error_embed, make_warning_embed
from utils.strings import S


InteractionHandler = Callable[[discord.Interaction], Awaitable[None]]


class BaseView(discord.ui.View):
    def __init__(self, author_id: int | None = None, timeout: float | None = 300):
        super().__init__(timeout=timeout)
        self.author_id = author_id
        self.message: discord.Message | None = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.author_id is None or interaction.user.id == self.author_id:
            return True
        if interaction.response.is_done():
            await interaction.followup.send(embed=make_warning_embed(S.NO_PERMISSION), ephemeral=True)
        else:
            await interaction.response.send_message(embed=make_warning_embed(S.NO_PERMISSION), ephemeral=True)
        return False

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        if self.message is None:
            return
        try:
            await self.message.edit(view=self)
        except (discord.HTTPException, discord.NotFound):
            return


class ConfirmView(BaseView):
    def __init__(
        self,
        author_id: int | None,
        on_confirm: InteractionHandler,
        on_cancel: InteractionHandler | None = None,
        timeout: float | None = 300,
    ) -> None:
        super().__init__(author_id=author_id, timeout=timeout)
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

    @discord.ui.button(label=S.CONFIRM, style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self.on_confirm(interaction)

    @discord.ui.button(label=S.CANCEL, style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        if self.on_cancel is None:
            if interaction.response.is_done():
                await interaction.followup.send(embed=make_warning_embed(S.CANCEL), ephemeral=True)
            else:
                await interaction.response.send_message(embed=make_warning_embed(S.CANCEL), ephemeral=True)
            return
        await self.on_cancel(interaction)


class BackToDashboardView(BaseView):
    def __init__(self, author_id: int, on_back: InteractionHandler) -> None:
        super().__init__(author_id=author_id, timeout=300)
        self.on_back = on_back

    @discord.ui.button(label=S.BACK_TO_DASHBOARD, style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self.on_back(interaction)


async def safe_send_error(interaction: discord.Interaction, message: str) -> None:
    embed = make_error_embed(message)
    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)
