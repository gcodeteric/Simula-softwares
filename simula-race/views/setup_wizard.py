from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

import discord

from utils.embeds import make_embed, make_success_embed
from utils.strings import S
from utils.validators import validate_hex_color, validate_non_empty
from views.common import BaseView


SetupCompleteHandler = Callable[[discord.Interaction, "SetupState"], Awaitable[None]]


@dataclass(slots=True)
class SetupState:
    league_name: str = ""
    sim: str = "ACC"
    timezone: str = "Europe/Lisbon"
    theme_key: str = "laranja_racing"
    primary_color: str = "#FF6600"
    secondary_color: str = "#1A1A2E"


def _setup_summary_embed(state: SetupState) -> discord.Embed:
    channels = "\n".join(f"• #{channel}" for channel in S.CHANNEL_PURPOSES.values())
    roles = "\n".join(f"• @{role}" for role in S.ROLE_NAME_MAP.values())
    return make_embed(
        S.SETUP_CHANNELS_CONFIRM.format(channels=channels, roles=roles),
        title=S.SETUP_STEP_CHANNELS,
    )


class SetupNameModal(discord.ui.Modal):
    def __init__(self, parent: "SetupWizardStep1") -> None:
        super().__init__(title=S.SETUP_STEP_NAME)
        self.parent = parent
        self.name_input = discord.ui.TextInput(
            label=S.SETUP_STEP_NAME,
            placeholder=S.SETUP_STEP_NAME_PLACEHOLDER,
            max_length=100,
        )
        self.add_item(self.name_input)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.parent.state.league_name = validate_non_empty(str(self.name_input.value))
        next_view = SetupWizardStep2(self.parent.author_id, self.parent.state, self.parent.on_complete)
        await interaction.response.edit_message(embed=make_embed(S.SETUP_STEP_SIM), view=next_view)


class SetupThemeModal(discord.ui.Modal):
    def __init__(self, parent: "SetupWizardStep4") -> None:
        super().__init__(title=S.SETUP_STEP_COLORS)
        self.parent = parent
        self.primary = discord.ui.TextInput(label=S.SETUP_THEME_PRIMARY_LABEL, placeholder="#FF6600", max_length=7)
        self.secondary = discord.ui.TextInput(label=S.SETUP_THEME_SECONDARY_LABEL, placeholder="#1A1A2E", max_length=7)
        self.add_item(self.primary)
        self.add_item(self.secondary)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.parent.state.primary_color = validate_hex_color(str(self.primary.value))
        self.parent.state.secondary_color = validate_hex_color(str(self.secondary.value))
        confirm_view = SetupWizardStep5(self.parent.author_id, self.parent.state, self.parent.on_complete)
        await interaction.response.edit_message(embed=_setup_summary_embed(self.parent.state), view=confirm_view)


class SetupWizardStep1(BaseView):
    def __init__(self, author_id: int, on_complete: SetupCompleteHandler, state: SetupState | None = None) -> None:
        super().__init__(author_id=author_id)
        self.state = state or SetupState()
        self.on_complete = on_complete

    @discord.ui.button(label=S.SETUP_DEFINE_NAME, style=discord.ButtonStyle.primary)
    async def set_name(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.send_modal(SetupNameModal(self))


class SetupWizardStep2(BaseView):
    def __init__(self, author_id: int, state: SetupState, on_complete: SetupCompleteHandler) -> None:
        super().__init__(author_id=author_id)
        self.state = state
        self.on_complete = on_complete
        for option in S.SIM_OPTIONS:
            button = discord.ui.Button(label=option, style=discord.ButtonStyle.primary if option == "ACC" else discord.ButtonStyle.secondary)
            button.callback = self._make_callback(option)
            self.add_item(button)

    def _make_callback(self, option: str):
        async def callback(interaction: discord.Interaction) -> None:
            self.state.sim = option
            next_view = SetupWizardStep3(self.author_id or interaction.user.id, self.state, self.on_complete)
            await interaction.response.edit_message(embed=make_embed(S.SETUP_STEP_TIMEZONE), view=next_view)

        return callback


class TimezoneSelect(discord.ui.Select):
    def __init__(self, parent: "SetupWizardStep3") -> None:
        options = [discord.SelectOption(label=tz, value=tz, default=tz == parent.state.timezone) for tz in S.TIMEZONE_OPTIONS]
        super().__init__(placeholder=S.SETUP_STEP_TIMEZONE, options=options, min_values=1, max_values=1)
        self.parent = parent

    async def callback(self, interaction: discord.Interaction) -> None:
        self.parent.state.timezone = str(self.values[0])
        next_view = SetupWizardStep4(self.parent.author_id or interaction.user.id, self.parent.state, self.parent.on_complete)
        await interaction.response.edit_message(embed=make_embed(S.SETUP_STEP_COLORS), view=next_view)


class SetupWizardStep3(BaseView):
    def __init__(self, author_id: int, state: SetupState, on_complete: SetupCompleteHandler) -> None:
        super().__init__(author_id=author_id)
        self.state = state
        self.on_complete = on_complete
        self.add_item(TimezoneSelect(self))


class SetupWizardStep4(BaseView):
    def __init__(self, author_id: int, state: SetupState, on_complete: SetupCompleteHandler) -> None:
        super().__init__(author_id=author_id)
        self.state = state
        self.on_complete = on_complete
        for theme_key, theme in S.COLOR_THEMES.items():
            button = discord.ui.Button(label=theme["name"], style=discord.ButtonStyle.secondary)
            button.callback = self._make_theme_callback(theme_key)
            self.add_item(button)
        custom_button = discord.ui.Button(label=S.SETUP_CUSTOM_THEME, style=discord.ButtonStyle.primary)
        custom_button.callback = self.custom_theme
        self.add_item(custom_button)

    def _make_theme_callback(self, theme_key: str):
        async def callback(interaction: discord.Interaction) -> None:
            theme = S.COLOR_THEMES[theme_key]
            self.state.theme_key = theme_key
            self.state.primary_color = theme["primary"]
            self.state.secondary_color = theme["secondary"]
            confirm_view = SetupWizardStep5(self.author_id or interaction.user.id, self.state, self.on_complete)
            await interaction.response.edit_message(embed=_setup_summary_embed(self.state), view=confirm_view)

        return callback

    async def custom_theme(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(SetupThemeModal(self))


class SetupWizardStep5(BaseView):
    def __init__(self, author_id: int, state: SetupState, on_complete: SetupCompleteHandler) -> None:
        super().__init__(author_id=author_id)
        self.state = state
        self.on_complete = on_complete

    @discord.ui.button(label=S.SETUP_CREATE_ALL, style=discord.ButtonStyle.success)
    async def create_all(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self.on_complete(interaction, self.state)

    @discord.ui.button(label=S.CANCEL, style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.edit_message(embed=make_success_embed(S.CANCEL), view=None)
