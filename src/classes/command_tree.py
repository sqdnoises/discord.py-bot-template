from typing import TYPE_CHECKING

from ..logger import logging

if TYPE_CHECKING:
    from .bot import Bot
    from .cog import Cog

from discord import app_commands
from discord.abc import Snowflake
from discord.ext import commands

__all__ = ("CommandTree",)


class CommandTree(app_commands.CommandTree):
    """Represents a container that holds application command information."""

    bot: "Bot"
    all_app_commands: dict[str, app_commands.AppCommand]

    def __init__(self, client: "Bot", *, fallback_to_global=True) -> None:
        super().__init__(client=client, fallback_to_global=fallback_to_global)
        self.bot = client
        self.all_app_commands = {}

    def _update_app_commands(
        self, cmds: list[app_commands.AppCommand]
    ) -> dict[str, app_commands.AppCommand]:
        self.all_app_commands = {cmd.name: cmd for cmd in cmds}
        return self.all_app_commands

    async def sync(
        self, *, guild: Snowflake | None = None
    ) -> list[app_commands.AppCommand]:
        logging.debug("syncing app commands...")
        cmds = await super().sync(guild=guild)
        self._update_app_commands(cmds)
        logging.debug(
            f"app commands synced & app commands list updated locally ({len(cmds)})"
        )
        return cmds

    async def update_app_commands(self) -> list[app_commands.AppCommand]:
        """Update local app commands list"""
        logging.debug("fetching app commands...")
        cmds = await self.fetch_commands()
        self._update_app_commands(cmds)
        logging.debug(
            f"app commands fetched & updated locally ({len(self.all_app_commands)})"
        )
        return cmds

    def slash_mention(self, qualified_command_name: str) -> str:
        """Mention an application command like a normal user or channel mention"""
        if qualified_command_name.startswith("/"):
            qualified_command_name = qualified_command_name[1:]
        parent = qualified_command_name.split(maxsplit=1)[0]
        return (
            f"</{qualified_command_name}:{self.all_app_commands[parent].id}>"
            if self.all_app_commands.get(parent)
            else f"`/{qualified_command_name}`"
        )

    def get_cog(
        self, command: app_commands.Command | commands.hybrid.HybridAppCommand
    ) -> "Cog | commands.Cog | None":
        """Get the cog that contains the app or hybrid command"""

        for cog in self.bot.cogs.values():
            if command in cog.get_app_commands():
                return cog

            if isinstance(command, commands.hybrid.HybridAppCommand):
                cmds = [
                    cmd.qualified_name
                    for cmd in cog.get_commands()
                    if isinstance(cmd, commands.HybridCommand)
                ]
                if command.qualified_name in cmds:
                    return cog

            if isinstance(command, commands.HybridCommand):
                if command in cog.get_commands():
                    return cog

        return None
