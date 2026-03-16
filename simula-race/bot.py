from __future__ import annotations

import asyncio
import logging

import discord
from discord import app_commands
from discord.ext import commands

from config import get_settings
from database.engine import init_models
from utils.embeds import make_error_embed
from utils.strings import S
from views.protest_views import AppealView, StewardVotingView
from views.rsvp_views import PersistentRSVPView


EXTENSIONS = (
    "cogs.admin",
    "cogs.dashboard",
    "cogs.registration",
    "cogs.stewarding",
    "cogs.results",
    "cogs.communication",
    "cogs.stats",
)


class LeagueBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        intents.messages = True
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)
        self.settings = get_settings()
        self.logger = logging.getLogger("league_bot")

    async def setup_hook(self) -> None:
        await init_models()
        for extension in EXTENSIONS:
            await self.load_extension(extension)
        self.add_view(PersistentRSVPView())
        self.add_view(StewardVotingView())
        self.add_view(AppealView())
        if self.settings.guild_id:
            guild = discord.Object(id=self.settings.guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

    async def on_ready(self) -> None:
        self.logger.info("Bot pronto como %s", self.user)

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
        message = str(error) or S.ERROR
        embed = make_error_embed(message)
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def main() -> None:
    settings = get_settings()
    if not settings.discord_bot_token:
        raise RuntimeError("DISCORD_BOT_TOKEN ou DISCORD_TOKEN é obrigatório.")
    logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
    bot = LeagueBot()
    async with bot:
        await bot.start(settings.discord_bot_token)


if __name__ == "__main__":
    asyncio.run(main())
