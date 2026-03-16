from __future__ import annotations

from collections.abc import Awaitable, Callable

import discord

from utils.strings import S
from views.common import BaseView


PublishHandler = Callable[[discord.Interaction], Awaitable[None]]
CorrectionHandler = Callable[[discord.Interaction, str], Awaitable[None]]
CancelHandler = Callable[[discord.Interaction], Awaitable[None]]


class ResultsCorrectionModal(discord.ui.Modal):
    def __init__(self, on_submit: CorrectionHandler) -> None:
        super().__init__(title=S.RESULTS_CORRECTION_MODAL)
        self.on_submit_handler = on_submit
        self.notes = discord.ui.TextInput(
            label=S.RESULTS_CORRECTION_LABEL,
            placeholder=S.RESULTS_CORRECTION_PLACEHOLDER,
            style=discord.TextStyle.paragraph,
            max_length=400,
        )
        self.add_item(self.notes)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.on_submit_handler(interaction, str(self.notes.value))


class ResultsPreviewView(BaseView):
    def __init__(
        self,
        author_id: int | None,
        on_publish: PublishHandler,
        on_correct: CorrectionHandler,
        on_cancel: CancelHandler,
    ) -> None:
        super().__init__(author_id=author_id, timeout=300)
        self.on_publish = on_publish
        self.on_correct = on_correct
        self.on_cancel = on_cancel

    @discord.ui.button(label=S.RESULTS_BTN_PUBLISH, style=discord.ButtonStyle.success)
    async def publish(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self.on_publish(interaction)

    @discord.ui.button(label=S.RESULTS_BTN_CORRECT, style=discord.ButtonStyle.primary)
    async def correct(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.send_modal(ResultsCorrectionModal(self.on_correct))

    @discord.ui.button(label=S.RESULTS_BTN_CANCEL, style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self.on_cancel(interaction)
