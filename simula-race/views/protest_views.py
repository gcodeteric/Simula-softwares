from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

import discord

from utils.embeds import make_embed
from utils.strings import S
from views.common import BaseView


ProtestCreateHandler = Callable[[discord.Interaction, "ProtestPayload"], Awaitable[None]]
VoteHandler = Callable[[discord.Interaction, str], Awaitable[None]]
PenaltyFinalizeHandler = Callable[[discord.Interaction, str, int, str], Awaitable[None]]
AppealHandler = Callable[[discord.Interaction, str], Awaitable[None]]


@dataclass(slots=True)
class ProtestPayload:
    accused_driver_id: int
    accused_label: str
    lap_number: int
    turn_zone: str
    description: str
    evidence_url: str


class ProtestDetailsModal(discord.ui.Modal):
    def __init__(self, parent: "ProtestWizardView", accused_driver_id: int, accused_label: str) -> None:
        super().__init__(title=S.PROTEST_MODAL_TITLE.format(n=parent.round_number))
        self.parent = parent
        self.accused_driver_id = accused_driver_id
        self.accused_label = accused_label
        self.lap_number = discord.ui.TextInput(label=S.PROTEST_FIELD_LAP, placeholder=S.PROTEST_FIELD_LAP_PLACEHOLDER, max_length=5)
        self.turn_zone = discord.ui.TextInput(label=S.PROTEST_FIELD_ZONE, placeholder=S.PROTEST_FIELD_ZONE_PLACEHOLDER, max_length=100)
        self.description_text = discord.ui.TextInput(
            label=S.PROTEST_FIELD_DESCRIPTION,
            placeholder=S.PROTEST_FIELD_DESCRIPTION_PLACEHOLDER,
            style=discord.TextStyle.paragraph,
            max_length=500,
        )
        self.evidence_url = discord.ui.TextInput(label=S.PROTEST_FIELD_EVIDENCE, placeholder=S.PROTEST_FIELD_EVIDENCE_PLACEHOLDER, max_length=200)
        for item in (self.lap_number, self.turn_zone, self.description_text, self.evidence_url):
            self.add_item(item)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        payload = ProtestPayload(
            accused_driver_id=self.accused_driver_id,
            accused_label=self.accused_label,
            lap_number=int(str(self.lap_number.value)),
            turn_zone=str(self.turn_zone.value),
            description=str(self.description_text.value),
            evidence_url=str(self.evidence_url.value),
        )
        preview = make_embed(
            S.PROTEST_SUCCESS.format(
                id="...",
                accused=payload.accused_label,
                n=self.parent.round_number,
                lap=payload.lap_number,
                zone=payload.turn_zone,
            )
        )
        await interaction.response.edit_message(
            embed=preview,
            view=ProtestConfirmView(self.parent.author_id or interaction.user.id, payload, self.parent.on_submit_handler),
        )


class ProtestAccusedSelect(discord.ui.Select):
    def __init__(self, parent: "ProtestWizardView") -> None:
        options = [discord.SelectOption(label=label, value=str(driver_id)) for driver_id, label in parent.accused_options[:25]]
        super().__init__(placeholder=S.PROTEST_FIELD_ACCUSED, options=options, min_values=1, max_values=1)
        self.parent = parent

    async def callback(self, interaction: discord.Interaction) -> None:
        accused_driver_id = int(self.values[0])
        accused_label = next(label for driver_id, label in self.parent.accused_options if driver_id == accused_driver_id)
        await interaction.response.send_modal(ProtestDetailsModal(self.parent, accused_driver_id, accused_label))


class ProtestWizardView(BaseView):
    def __init__(
        self,
        author_id: int,
        round_number: int,
        accused_options: list[tuple[int, str]],
        on_submit: ProtestCreateHandler,
    ) -> None:
        super().__init__(author_id=author_id, timeout=300)
        self.round_number = round_number
        self.accused_options = accused_options
        self.on_submit_handler = on_submit
        self.add_item(ProtestAccusedSelect(self))


class ProtestConfirmView(BaseView):
    def __init__(self, author_id: int, payload: ProtestPayload, on_submit: ProtestCreateHandler) -> None:
        super().__init__(author_id=author_id, timeout=300)
        self.payload = payload
        self.on_submit_handler = on_submit

    @discord.ui.button(label=S.CONFIRM, style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self.on_submit_handler(interaction, self.payload)

    @discord.ui.button(label=S.CANCEL, style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.edit_message(view=None)


class StewardVotingView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    async def _dispatch(self, interaction: discord.Interaction, action: str) -> None:
        cog = interaction.client.get_cog("StewardingCog")
        if cog is None:
            return
        await cog.handle_steward_action(interaction, action)

    @discord.ui.button(label=S.STEWARD_BTN_CLAIM, style=discord.ButtonStyle.primary, custom_id="steward_claim")
    async def claim(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self._dispatch(interaction, "claim")

    @discord.ui.button(label=S.STEWARD_BTN_GUILTY, style=discord.ButtonStyle.success, custom_id="steward_guilty")
    async def guilty(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self._dispatch(interaction, "guilty")

    @discord.ui.button(label=S.STEWARD_BTN_NOT_GUILTY, style=discord.ButtonStyle.secondary, custom_id="steward_not_guilty")
    async def not_guilty(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self._dispatch(interaction, "not_guilty")

    @discord.ui.button(label=S.STEWARD_BTN_RACING_INCIDENT, style=discord.ButtonStyle.secondary, custom_id="steward_racing_incident")
    async def racing_incident(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self._dispatch(interaction, "racing_incident")

    @discord.ui.button(label=S.STEWARD_BTN_DISMISS, style=discord.ButtonStyle.danger, custom_id="steward_dismiss")
    async def dismiss(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self._dispatch(interaction, "dismiss")


class PenaltyReasoningModal(discord.ui.Modal):
    def __init__(self, parent: "PenaltySelectView") -> None:
        super().__init__(title=S.STEWARD_REASONING_TITLE)
        self.parent = parent
        self.reasoning = discord.ui.TextInput(
            label=S.STEWARD_REASONING_TITLE,
            placeholder=S.STEWARD_REASONING_PLACEHOLDER,
            style=discord.TextStyle.paragraph,
            max_length=500,
        )
        self.add_item(self.reasoning)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.parent.on_submit_handler(
            interaction,
            self.parent.penalty_value,
            self.parent.pp_value,
            str(self.reasoning.value),
        )


class PenaltyTypeSelect(discord.ui.Select):
    def __init__(self, parent: "PenaltySelectView") -> None:
        super().__init__(
            placeholder=S.STEWARD_PENALTY_TITLE,
            options=[
                discord.SelectOption(label=S.STEWARD_PENALTY_WARNING, value="warning"),
                discord.SelectOption(label=S.STEWARD_PENALTY_5S, value="+5s"),
                discord.SelectOption(label=S.STEWARD_PENALTY_10S, value="+10s"),
                discord.SelectOption(label=S.STEWARD_PENALTY_30S, value="+30s"),
                discord.SelectOption(label=S.STEWARD_PENALTY_GRID3, value="grid-3"),
                discord.SelectOption(label=S.STEWARD_PENALTY_GRID5, value="grid-5"),
                discord.SelectOption(label=S.STEWARD_PENALTY_DSQ, value="dsq"),
                discord.SelectOption(label=S.STEWARD_PENALTY_SUSPENSION, value="suspension"),
                discord.SelectOption(label=S.STEWARD_PENALTY_BAN, value="ban"),
            ],
        )
        self.parent = parent

    async def callback(self, interaction: discord.Interaction) -> None:
        self.parent.penalty_value = str(self.values[0])
        await interaction.response.defer()


class PenaltyPPSelect(discord.ui.Select):
    def __init__(self, parent: "PenaltySelectView") -> None:
        super().__init__(
            placeholder=S.STEWARD_PP_TITLE,
            options=[discord.SelectOption(label=str(value), value=str(value)) for value in range(0, 6)],
        )
        self.parent = parent

    async def callback(self, interaction: discord.Interaction) -> None:
        self.parent.pp_value = int(self.values[0])
        await interaction.response.defer()


class PenaltySelectView(BaseView):
    def __init__(self, author_id: int | None, on_submit: PenaltyFinalizeHandler) -> None:
        super().__init__(author_id=author_id, timeout=300)
        self.on_submit_handler = on_submit
        self.penalty_value = "warning"
        self.pp_value = 0
        self.add_item(PenaltyTypeSelect(self))
        self.add_item(PenaltyPPSelect(self))

    @discord.ui.button(label=S.CONFIRM, style=discord.ButtonStyle.success)
    async def continue_flow(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.send_modal(PenaltyReasoningModal(self))


class AppealModal(discord.ui.Modal):
    def __init__(self, protest_id: int, on_submit: AppealHandler) -> None:
        super().__init__(title=S.APPEAL_MODAL_TITLE.format(id=protest_id))
        self.protest_id = protest_id
        self.on_submit_handler = on_submit
        self.reason = discord.ui.TextInput(
            label=S.APPEAL_MODAL_TITLE.format(id=protest_id),
            placeholder=S.APPEAL_MODAL_PLACEHOLDER,
            style=discord.TextStyle.paragraph,
            max_length=500,
        )
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.on_submit_handler(interaction, str(self.reason.value))


class AppealView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label=S.APPEAL_BTN, style=discord.ButtonStyle.primary, custom_id="appeal_submit")
    async def appeal(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        cog = interaction.client.get_cog("StewardingCog")
        if cog is None:
            return
        await cog.handle_appeal_button(interaction)
