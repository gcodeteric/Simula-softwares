from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

import discord

from utils.embeds import make_embed
from utils.strings import S
from utils.time_utils import format_date_time
from utils.validators import validate_non_empty, validate_round_datetime
from views.common import BaseView


RoundCompleteHandler = Callable[[discord.Interaction, "RoundState"], Awaitable[None]]


@dataclass(slots=True)
class RoundState:
    round_number: int | None = None
    track_name: str = ""
    track_country: str | None = None
    track_flag: str | None = None
    date_time: object | None = None
    format: str = "sprint"
    start_type: str = "rolling"
    race_duration_min: int = 40
    weather: str = "dry"


class RoundTrackModal(discord.ui.Modal):
    def __init__(self, parent: "RoundWizardStep2") -> None:
        super().__init__(title=S.ROUND_STEP_TRACK)
        self.parent = parent
        self.track = discord.ui.TextInput(
            label=S.ROUND_STEP_TRACK,
            placeholder=S.ROUND_STEP_TRACK_PLACEHOLDER,
            max_length=100,
        )
        self.add_item(self.track)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        raw_track = validate_non_empty(str(self.track.value))
        match = next(
            (item for item in self.parent.tracks if raw_track.lower() in str(item["name"]).lower()),
            None,
        )
        if match is None:
            match = {"name": raw_track, "country": None, "flag": ""}
        self.parent.state.track_name = str(match["name"])
        self.parent.state.track_country = str(match.get("country") or "")
        self.parent.state.track_flag = str(match.get("flag") or "")
        await interaction.response.edit_message(
            embed=make_embed(S.ROUND_STEP_DATE, title=S.ROUND_WIZARD_TITLE),
            view=RoundWizardStep3(self.parent.author_id or interaction.user.id, self.parent.state, self.parent.on_complete, self.parent.tracks),
        )


class RoundDateTimeModal(discord.ui.Modal):
    def __init__(self, parent: "RoundWizardStep3", timezone_name: str) -> None:
        super().__init__(title=S.ROUND_STEP_DATE)
        self.parent = parent
        self.timezone_name = timezone_name
        self.date_value = discord.ui.TextInput(label=S.ROUND_FIELD_DATE, placeholder="2026-04-20", max_length=10)
        self.time_value = discord.ui.TextInput(label=S.ROUND_FIELD_TIME, placeholder="21:00", max_length=5)
        self.add_item(self.date_value)
        self.add_item(self.time_value)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.parent.state.date_time = validate_round_datetime(
            str(self.date_value.value),
            str(self.time_value.value),
            self.timezone_name,
        )
        await interaction.response.edit_message(
            embed=make_embed(S.ROUND_STEP_DETAILS, title=S.ROUND_WIZARD_TITLE),
            view=RoundWizardStep4(self.parent.author_id or interaction.user.id, self.parent.state, self.parent.on_complete),
        )


class RoundWizardStep1(BaseView):
    def __init__(self, author_id: int, on_complete: RoundCompleteHandler, available_numbers: list[int], tracks: list[dict[str, object]], timezone_name: str) -> None:
        super().__init__(author_id=author_id)
        self.state = RoundState()
        self.on_complete = on_complete
        self.available_numbers = available_numbers
        self.tracks = tracks
        self.timezone_name = timezone_name
        options = [discord.SelectOption(label=str(number), value=str(number)) for number in available_numbers[:25]]
        self.add_item(RoundNumberSelect(self, options))


class RoundNumberSelect(discord.ui.Select):
    def __init__(self, parent: RoundWizardStep1, options: list[discord.SelectOption]) -> None:
        super().__init__(placeholder=S.ROUND_STEP_NUMBER, options=options, min_values=1, max_values=1)
        self.parent = parent

    async def callback(self, interaction: discord.Interaction) -> None:
        self.parent.state.round_number = int(self.values[0])
        await interaction.response.edit_message(
            embed=make_embed(S.ROUND_STEP_TRACK, title=S.ROUND_WIZARD_TITLE),
            view=RoundWizardStep2(
                self.parent.author_id or interaction.user.id,
                self.parent.state,
                self.parent.on_complete,
                self.parent.tracks,
                self.parent.timezone_name,
            ),
        )


class RoundWizardStep2(BaseView):
    def __init__(self, author_id: int, state: RoundState, on_complete: RoundCompleteHandler, tracks: list[dict[str, object]], timezone_name: str) -> None:
        super().__init__(author_id=author_id)
        self.state = state
        self.on_complete = on_complete
        self.tracks = tracks
        self.timezone_name = timezone_name

    @discord.ui.button(label=S.ROUND_SET_TRACK, style=discord.ButtonStyle.primary)
    async def set_track(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.send_modal(RoundTrackModal(self))


class RoundWizardStep3(BaseView):
    def __init__(self, author_id: int, state: RoundState, on_complete: RoundCompleteHandler, tracks: list[dict[str, object]], timezone_name: str) -> None:
        super().__init__(author_id=author_id)
        self.state = state
        self.on_complete = on_complete
        self.tracks = tracks
        self.timezone_name = timezone_name

    @discord.ui.button(label=S.ROUND_SET_DATETIME, style=discord.ButtonStyle.primary)
    async def set_datetime(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await interaction.response.send_modal(RoundDateTimeModal(self, self.timezone_name))


class RoundWizardStep4(BaseView):
    def __init__(self, author_id: int, state: RoundState, on_complete: RoundCompleteHandler) -> None:
        super().__init__(author_id=author_id)
        self.state = state
        self.on_complete = on_complete
        self.add_item(RoundFormatSelect(self))
        self.add_item(RoundWeatherSelect(self))
        self.add_item(RoundStartSelect(self))
        self.add_item(RoundDurationSelect(self))

    @discord.ui.button(label=S.ROUND_CREATE, style=discord.ButtonStyle.success, row=4)
    async def create(self, interaction: discord.Interaction, _: discord.ui.Button) -> None:
        await self.on_complete(interaction, self.state)


class RoundFormatSelect(discord.ui.Select):
    def __init__(self, parent: RoundWizardStep4) -> None:
        super().__init__(
            placeholder=S.ROUND_FORMAT_SPRINT,
            options=[
                discord.SelectOption(label=S.ROUND_FORMAT_SPRINT, value="sprint"),
                discord.SelectOption(label=S.ROUND_FORMAT_ENDURANCE, value="endurance"),
            ],
        )
        self.parent = parent

    async def callback(self, interaction: discord.Interaction) -> None:
        self.parent.state.format = str(self.values[0])
        await interaction.response.defer()


class RoundWeatherSelect(discord.ui.Select):
    def __init__(self, parent: RoundWizardStep4) -> None:
        super().__init__(
            placeholder=S.ROUND_WEATHER_DRY,
            options=[
                discord.SelectOption(label=S.ROUND_WEATHER_DRY, value="dry"),
                discord.SelectOption(label=S.ROUND_WEATHER_RAIN, value="rain"),
                discord.SelectOption(label=S.ROUND_WEATHER_DYNAMIC, value="dynamic"),
                discord.SelectOption(label=S.ROUND_WEATHER_RANDOM, value="random"),
            ],
        )
        self.parent = parent

    async def callback(self, interaction: discord.Interaction) -> None:
        self.parent.state.weather = str(self.values[0])
        await interaction.response.defer()


class RoundStartSelect(discord.ui.Select):
    def __init__(self, parent: RoundWizardStep4) -> None:
        super().__init__(
            placeholder=S.ROUND_START_ROLLING,
            options=[
                discord.SelectOption(label=S.ROUND_START_ROLLING, value="rolling"),
                discord.SelectOption(label=S.ROUND_START_STANDING, value="standing"),
            ],
        )
        self.parent = parent

    async def callback(self, interaction: discord.Interaction) -> None:
        self.parent.state.start_type = str(self.values[0])
        await interaction.response.defer()


class RoundDurationSelect(discord.ui.Select):
    def __init__(self, parent: RoundWizardStep4) -> None:
        super().__init__(
            placeholder=S.ROUND_DURATION_PLACEHOLDER,
            options=[
                discord.SelectOption(label=S.ROUND_DURATION_30, value="30"),
                discord.SelectOption(label=S.ROUND_DURATION_40, value="40"),
                discord.SelectOption(label=S.ROUND_DURATION_60, value="60"),
                discord.SelectOption(label=S.ROUND_DURATION_90, value="90"),
            ],
        )
        self.parent = parent

    async def callback(self, interaction: discord.Interaction) -> None:
        self.parent.state.race_duration_min = int(self.values[0])
        await interaction.response.defer()


def round_created_embed(state: RoundState) -> discord.Embed:
    date_value, time_value = format_date_time(state.date_time) if state.date_time else ("", "")
    return make_embed(
        S.ROUND_CREATED.format(
            n=state.round_number,
            track=state.track_name,
            flag=state.track_flag or "",
            date=date_value,
            time=time_value,
            weather=state.weather,
            duration=state.race_duration_min,
            format=state.format,
        ),
        title=S.ROUND_WIZARD_TITLE,
    )
