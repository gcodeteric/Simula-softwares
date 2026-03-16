from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

import discord

from utils.embeds import make_embed
from utils.strings import S
from utils.validators import validate_non_empty
from views.common import BaseView


SeasonCompleteHandler = Callable[[discord.Interaction, "SeasonState"], Awaitable[None]]


@dataclass(slots=True)
class SeasonState:
    name: str = ""
    sim: str = "ACC"
    num_rounds: int = 10
    drops: int = 2
    points_system_id: int | None = None
    points_system_name: str = ""


class SeasonNameModal(discord.ui.Modal):
    def __init__(self, parent: "SeasonWizardStep1") -> None:
        super().__init__(title=S.SEASON_STEP_NAME)
        self.parent = parent
        self.name_input = discord.ui.TextInput(
            label=S.SEASON_STEP_NAME,
            placeholder=S.SEASON_STEP_NAME_PLACEHOLDER,
            max_length=100,
        )
        self.add_item(self.name_input)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.parent.state.name = validate_non_empty(str(self.name_input.value))
        await interaction.response.edit_message(
            embed=make_embed(S.SEASON_STEP_SIM, title=S.SEASON_WIZARD_TITLE),
            view=SeasonWizardStep2(self.parent.author_id or interaction.user.id, self.parent.state, self.parent.on_complete, self.parent.points_systems),
        )


class SeasonRoundsModal(discord.ui.Modal):
    def __init__(self, parent: "SeasonWizardStep3") -> None:
        super().__init__(title=S.SEASON_STEP_ROUNDS)
        self.parent = parent
        self.rounds = discord.ui.TextInput(label=S.SEASON_STEP_ROUNDS, placeholder="10", max_length=2)
        self.add_item(self.rounds)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.parent.state.num_rounds = int(str(self.rounds.value))
        await interaction.response.edit_message(
            embed=make_embed(f"{S.SEASON_STEP_DROPS}\n\n{S.SEASON_STEP_DROPS_HELP}", title=S.SEASON_WIZARD_TITLE),
            view=SeasonWizardStep4(self.parent.author_id or interaction.user.id, self.parent.state, self.parent.on_complete, self.parent.points_systems),
        )


class PointsSystemSelect(discord.ui.Select):
    def __init__(self, parent: "SeasonWizardStep5", options_data: list[dict[str, object]]) -> None:
        options = [
            discord.SelectOption(label=str(item["name"]), value=str(item["id"]), description=str(item["description"])[:100])
            for item in options_data[:25]
        ]
        super().__init__(placeholder=S.SEASON_STEP_POINTS, options=options, min_values=1, max_values=1)
        self.parent = parent
        self.options_data = {str(item["id"]): item for item in options_data}

    async def callback(self, interaction: discord.Interaction) -> None:
        selected = self.options_data[str(self.values[0])]
        self.parent.state.points_system_id = int(selected["id"])
        self.parent.state.points_system_name = str(selected["name"])
        await interaction.response.edit_message(
            embed=self.parent.build_confirm_embed(),
            view=SeasonWizardStep6(self.parent.author_id or interaction.user.id, self.parent.state, self.parent.on_complete),
        )


class SeasonWizardStep1(BaseView):
    def __init__(self, author_id: int, on_complete: SeasonCompleteHandler, points_systems: list[dict[str, object]]) -> None:
        super().__init__(author_id=author_id)
        self.state = SeasonState()
        self.on_complete = on_complete
        self.points_systems = points_systems

    @discord.ui.button(label=S.SETUP_DEFINE_NAME, style=discord.ButtonStyle.primary)
    async def set_name(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.send_modal(SeasonNameModal(self))


class SeasonWizardStep2(BaseView):
    def __init__(self, author_id: int, state: SeasonState, on_complete: SeasonCompleteHandler, points_systems: list[dict[str, object]]) -> None:
        super().__init__(author_id=author_id)
        self.state = state
        self.on_complete = on_complete
        self.points_systems = points_systems
        for option in S.SIM_OPTIONS[:-1]:
            button = discord.ui.Button(label=option, style=discord.ButtonStyle.secondary)
            button.callback = self._make_callback(option)
            self.add_item(button)

    def _make_callback(self, option: str):
        async def callback(interaction: discord.Interaction) -> None:
            self.state.sim = option
            await interaction.response.edit_message(
                embed=make_embed(S.SEASON_STEP_ROUNDS, title=S.SEASON_WIZARD_TITLE),
                view=SeasonWizardStep3(self.author_id or interaction.user.id, self.state, self.on_complete, self.points_systems),
            )

        return callback


class SeasonWizardStep3(BaseView):
    def __init__(self, author_id: int, state: SeasonState, on_complete: SeasonCompleteHandler, points_systems: list[dict[str, object]]) -> None:
        super().__init__(author_id=author_id)
        self.state = state
        self.on_complete = on_complete
        self.points_systems = points_systems
        for round_count in (6, 8, 10, 12):
            button = discord.ui.Button(label=str(round_count), style=discord.ButtonStyle.secondary)
            button.callback = self._make_callback(round_count)
            self.add_item(button)
        other = discord.ui.Button(label=S.SEASON_CUSTOM_ROUNDS, style=discord.ButtonStyle.primary)
        other.callback = self.other_rounds
        self.add_item(other)

    def _make_callback(self, round_count: int):
        async def callback(interaction: discord.Interaction) -> None:
            self.state.num_rounds = round_count
            await interaction.response.edit_message(
                embed=make_embed(f"{S.SEASON_STEP_DROPS}\n\n{S.SEASON_STEP_DROPS_HELP}", title=S.SEASON_WIZARD_TITLE),
                view=SeasonWizardStep4(self.author_id or interaction.user.id, self.state, self.on_complete, self.points_systems),
            )

        return callback

    async def other_rounds(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(SeasonRoundsModal(self))


class SeasonWizardStep4(BaseView):
    def __init__(self, author_id: int, state: SeasonState, on_complete: SeasonCompleteHandler, points_systems: list[dict[str, object]]) -> None:
        super().__init__(author_id=author_id)
        self.state = state
        self.on_complete = on_complete
        self.points_systems = points_systems
        for drops in (0, 1, 2, 3):
            button = discord.ui.Button(label=str(drops), style=discord.ButtonStyle.secondary)
            button.callback = self._make_callback(drops)
            self.add_item(button)

    def _make_callback(self, drops: int):
        async def callback(interaction: discord.Interaction) -> None:
            self.state.drops = drops
            await interaction.response.edit_message(
                embed=make_embed(S.SEASON_STEP_POINTS, title=S.SEASON_WIZARD_TITLE),
                view=SeasonWizardStep5(self.author_id or interaction.user.id, self.state, self.on_complete, self.points_systems),
            )

        return callback


class SeasonWizardStep5(BaseView):
    def __init__(self, author_id: int, state: SeasonState, on_complete: SeasonCompleteHandler, points_systems: list[dict[str, object]]) -> None:
        super().__init__(author_id=author_id)
        self.state = state
        self.on_complete = on_complete
        self.points_systems = points_systems
        self.add_item(PointsSystemSelect(self, points_systems))

    def build_confirm_embed(self) -> discord.Embed:
        return make_embed(
            S.SEASON_CREATED.format(
                name=self.state.name,
                sim=self.state.sim,
                rounds=self.state.num_rounds,
                drops=self.state.drops,
                points=self.state.points_system_name,
            ),
            title=S.SEASON_STEP_CONFIRM,
        )


class SeasonWizardStep6(BaseView):
    def __init__(self, author_id: int, state: SeasonState, on_complete: SeasonCompleteHandler) -> None:
        super().__init__(author_id=author_id)
        self.state = state
        self.on_complete = on_complete

    @discord.ui.button(label=S.SEASON_CREATE, style=discord.ButtonStyle.success)
    async def create(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self.on_complete(interaction, self.state)

    @discord.ui.button(label=S.CANCEL, style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.edit_message(view=None)
