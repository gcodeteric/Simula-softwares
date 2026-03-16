from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

import discord

from utils.strings import S
from views.common import BaseView


RegistrationHandler = Callable[[discord.Interaction, "RegistrationPayload"], Awaitable[None]]
DecisionHandler = Callable[[discord.Interaction, int, str], Awaitable[None]]
ProfileHandler = Callable[[discord.Interaction, int], Awaitable[None]]


@dataclass(slots=True)
class RegistrationPayload:
    real_name: str | None
    game_id: str
    car_number: int
    team_name: str | None
    nationality: str | None


class RegistrationModal(discord.ui.Modal):
    def __init__(self, season_name: str, on_submit: RegistrationHandler) -> None:
        super().__init__(title=S.REGISTER_MODAL_TITLE.format(season_name=season_name))
        self.on_submit_handler = on_submit
        self.real_name = discord.ui.TextInput(
            label=S.REGISTER_FIELD_NAME,
            placeholder=S.REGISTER_FIELD_NAME_PLACEHOLDER,
            required=False,
            max_length=100,
        )
        self.game_id = discord.ui.TextInput(
            label=S.REGISTER_FIELD_GAMEID,
            placeholder=S.REGISTER_FIELD_GAMEID_PLACEHOLDER,
            max_length=64,
        )
        self.car_number = discord.ui.TextInput(
            label=S.REGISTER_FIELD_CAR_NUMBER,
            placeholder=S.REGISTER_FIELD_CAR_NUMBER_PLACEHOLDER,
            max_length=3,
        )
        self.team_name = discord.ui.TextInput(
            label=S.REGISTER_FIELD_TEAM,
            placeholder=S.REGISTER_FIELD_TEAM_PLACEHOLDER,
            required=False,
            max_length=100,
        )
        self.nationality = discord.ui.TextInput(
            label=S.REGISTER_FIELD_NATIONALITY,
            placeholder=S.REGISTER_FIELD_NATIONALITY_PLACEHOLDER,
            required=False,
            max_length=64,
        )
        for item in (self.real_name, self.game_id, self.car_number, self.team_name, self.nationality):
            self.add_item(item)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        payload = RegistrationPayload(
            real_name=str(self.real_name.value).strip() or None,
            game_id=str(self.game_id.value).strip(),
            car_number=int(str(self.car_number.value)),
            team_name=str(self.team_name.value).strip() or None,
            nationality=str(self.nationality.value).strip() or None,
        )
        await self.on_submit_handler(interaction, payload)


class RegistrationEntryView(BaseView):
    def __init__(self, author_id: int, season_name: str, on_submit: RegistrationHandler) -> None:
        super().__init__(author_id=author_id, timeout=300)
        self.season_name = season_name
        self.on_submit_handler = on_submit

    @discord.ui.button(label=S.REGISTER_BTN, style=discord.ButtonStyle.primary)
    async def open_modal(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.send_modal(RegistrationModal(self.season_name, self.on_submit_handler))


class RejectionReasonModal(discord.ui.Modal):
    def __init__(self, registration_id: int, on_decision: DecisionHandler) -> None:
        super().__init__(title=S.REJECT_MODAL_TITLE)
        self.registration_id = registration_id
        self.on_decision = on_decision
        self.reason = discord.ui.TextInput(label=S.REJECT_MODAL_TITLE, placeholder=S.REJECT_MODAL_PLACEHOLDER, max_length=200)
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await self.on_decision(interaction, self.registration_id, str(self.reason.value))


class ApprovalView(BaseView):
    def __init__(self, registration_id: int, on_approve: DecisionHandler, on_reject: DecisionHandler, on_profile: ProfileHandler) -> None:
        super().__init__(author_id=None, timeout=300)
        self.registration_id = registration_id
        self.on_approve = on_approve
        self.on_reject = on_reject
        self.on_profile = on_profile

    @discord.ui.button(label=S.APPROVE_BTN_APPROVE, style=discord.ButtonStyle.success)
    async def approve(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self.on_approve(interaction, self.registration_id, "")

    @discord.ui.button(label=S.APPROVE_BTN_REJECT, style=discord.ButtonStyle.danger)
    async def reject(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.send_modal(RejectionReasonModal(self.registration_id, self.on_reject))

    @discord.ui.button(label=S.APPROVE_BTN_PROFILE, style=discord.ButtonStyle.secondary)
    async def profile(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self.on_profile(interaction, self.registration_id)
