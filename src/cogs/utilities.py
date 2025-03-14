import asyncio
from typing import Literal, Iterable

from .. import utils
from ..classes import Bot, Cog
from ..views.utilities import InstallView

import psutil
from ping3 import ping

import discord
from discord import app_commands


class Utilities(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.process = psutil.Process()

    def get_latency_circle(self, latency: float | None) -> str:
        if latency is None:
            return "⚫"
        elif latency <= 0:
            return "⚪"
        elif latency <= 0.1:
            return "🟢"
        elif latency <= 0.35:
            return "🟡"
        else:
            return "🔴"

    async def measure_ping(
        self, domains: Iterable[str]
    ) -> dict[str, float | Literal[False] | None]:
        """Measure the ping"""

        async def get_ping(domain: str) -> float | Literal[False] | None:
            return await self.run(ping, domain)

        pings = await asyncio.gather(*[get_ping(domain) for domain in domains])

        return {
            domain: ping for domain, ping in zip(domains, pings)  # False means error
        }

    @app_commands.command(
        name="ping",
        description="Check the latency of the bot and the services being used",
    )
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def ping(self, interaction: discord.Interaction) -> None:
        # Defer the response
        ephemeral = False
        if isinstance(interaction.channel, discord.abc.PrivateChannel):
            ephemeral = True
        await interaction.response.defer(ephemeral=ephemeral)

        def add_ping_field(
            name: str, latency: float | Literal[False] | None
        ) -> discord.Embed:
            if latency is None:
                value = f"`{self.get_latency_circle(None)} Unreachable`"
            elif latency is False:
                value = f"`{self.get_latency_circle(None)} Error`"
            else:
                ping_text = (
                    f"{round(latency*1000)}ms" if latency < 1000 else f"{latency:.2f}s"
                )
                value = f"`{self.get_latency_circle(latency)} " + ping_text + "`"

            return embed.add_field(name=name, value=value)

        # Create the embed
        embed = discord.Embed(
            title="Pong! 🏓",
            color=discord.Color.dark_green(),
            timestamp=discord.utils.utcnow(),
        )

        domains = {"discord.com": "Discord"}

        pings = await self.measure_ping(domains)
        add_ping_field(list(domains.values())[0], pings.pop(list(domains.keys())[0]))

        bot_ping_text = (
            f"{round(interaction.client.latency*1000)}ms"
            if interaction.client.latency < 1000
            else f"{interaction.client.latency:.2f}s"
        )
        embed.add_field(
            name="Discord WS Latency",
            value=f"`{self.get_latency_circle(interaction.client.latency)} "
            + bot_ping_text
            + "`",
        )

        for domain, ping in pings.items():
            add_ping_field(domains[domain], ping)

        for i in range((len(embed.fields) // 2)):
            embed.insert_field_at(i * 2 + 2 + i, name="", value="")

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="statistics", description="Statistics about the bot")
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def statistics(self, interaction: discord.Interaction) -> None:
        assert self.bot.user is not None
        assert self.bot.uptime is not None

        embed = discord.Embed(
            title=f"🌟 {self.bot.user.display_name} Statistics",
            timestamp=discord.utils.utcnow(),
            color=discord.Color.dark_green(),
        )

        embed.add_field(name="Servers", value=f"`{len(self.bot.guilds):,}`")

        embed.add_field(name="Users", value=f"`{len(self.bot.users):,}`")

        embed.add_field(name="Platform", value=f"`{utils.detect_platform()}`")

        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_count = psutil.cpu_count()
        cpu_usage = self.process.cpu_percent() / (cpu_count or 1)

        embed.add_field(
            name="Process",
            value=f"`{cpu_usage:.2f}%` (cpu)\n"
            f"`{round(memory_usage)} MiB` (memory)\n"
            f"up since <t:{int(self.bot.uptime.timestamp())}:R>",
        )

        embed.add_field(
            name="Ping", value=f"Check with {self.bot.slash_mention('ping')}"
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar)

        ephemeral = False
        if isinstance(interaction.channel, discord.abc.PrivateChannel):
            ephemeral = True
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

    @app_commands.command(
        name="install",
        description="Provide a link to install the bot in a user or invite it to a server",
    )
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    async def install(self, interaction: discord.Interaction) -> None:
        assert self.bot.user is not None
        assert self.bot.application_id is not None

        embed = discord.Embed(
            title=f"Install {self.bot.user.display_name}",
            description=f"Click the buttons below to add **{self.bot.user.display_name}** in your apps and use it anywhere or invite it to your server.",
            color=discord.Color.dark_green(),
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar)

        view = InstallView(self.bot.application_id)
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Utilities(bot))
