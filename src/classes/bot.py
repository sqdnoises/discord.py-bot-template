import sys
import logging
import pkg_resources
from typing import TYPE_CHECKING, Optional
from datetime import datetime

from .. import cogs
from .. import utils
from ..config import BOT_NAME, LOG_CHANNEL, COGS_EXCLUDE
from ..utils import get_logger, mprint
from ..termcolors import *

from .context import Context
from .command_tree import CommandTree

if TYPE_CHECKING:
    from .custom_types import ContextT_co, PrefixType

from prisma import Prisma

import discord
from discord import app_commands
from discord.ext import commands

__all__ = ("Bot",)

logger = get_logger()


class Bot(commands.Bot):
    tree: CommandTree
    uptime: datetime | None
    prisma: Prisma
    log_channel: Optional[discord.TextChannel]
    log_channel_id: Optional[int]
    all_app_commands: dict[str, app_commands.AppCommand]

    def __init__(
        self,
        command_prefix: "PrefixType",
        *args,
        intents: discord.Intents = discord.Intents.all(),
        tree_cls: type[app_commands.CommandTree] = CommandTree,
        **kwargs,
    ) -> None:
        super().__init__(
            command_prefix=command_prefix,
            intents=intents,
            tree_cls=tree_cls,
            *args,
            **kwargs,
            help_command=commands.DefaultHelpCommand(),
        )
        self.uptime = None
        self.prisma = Prisma(auto_register=True)

        self.log_channel_id = LOG_CHANNEL
        self.log_channel = None

    async def connect_db(self) -> None:
        if self.prisma.is_connected():
            logger.warning("tried to connect to database while already connected")
            return

        await self.prisma.connect()
        logger.info("connected to database")

    async def disconnect_db(self) -> None:
        if not self.prisma.is_connected():
            logger.warning(
                "tried to disconnect from database while already disconnected"
            )
            return

        await self.prisma.disconnect()
        logger.info("disconnected from database")

    async def enable_wal_mode(self) -> None:
        try:
            await self.prisma.execute_raw("PRAGMA journal_mode=WAL;")
            print("SQLite3 journal mode set to WAL.")
        except Exception as e:
            print(f"Error setting WAL mode: {e}")

    async def _load_all_cogs(self) -> None:
        loaded = []
        excluded = []

        exclude = COGS_EXCLUDE
        for module in utils.list_modules(cogs):
            module_imported = utils.import_submodule(module)

            if (
                module in exclude
                or module.replace(cogs.__package__ + ".", "", 1) in exclude  # type: ignore
            ):
                excluded.append(
                    module + f" {rgb(49, 49, 49)}(excluded in config){reset}"
                )
                continue

            if hasattr(module_imported, "__ignore__") and getattr(
                module_imported, "__ignore__"
            ):
                excluded.append(module + f" {rgb(49, 49, 49)}(ignored){reset}")
                continue

            try:
                await self.load_extension(module)

            except commands.NoEntryPointError:
                logger.warning(
                    f"excluding `{module}` because there is no entry point (no 'setup' function found)"
                )
                excluded.append(
                    module + f" {rgb(49, 49, 49)}(no 'setup' function){reset}"
                )

            except Exception as e:
                logger.critical(
                    f"excluding `{module}` because there was an error while loading it (this may cause unintended behaviour)",
                    exc_info=e,
                )
                excluded.append(
                    module + f" {rgb(49, 49, 49)}(error: {e.__class__.__name__}){reset}"
                )

            else:
                loaded.append(module)

        loaded_paginated = utils.paginate(loaded, 3)
        excluded_paginated = utils.paginate(excluded, 2)
        prefix_length = 30 + len(BOT_NAME)

        loaded_str = f"the following cogs have been {underline}loaded{reset}:\n"
        for x in loaded_paginated:
            loaded_str += (" " * prefix_length) + f"{', '.join(x)}\n"

        excluded_str = f"the following cogs have been {underline}excluded{reset}:\n"
        for x in excluded_paginated:
            excluded_str += (" " * prefix_length) + f"{', '.join(x)}\n"

        logger.info(loaded_str.strip())
        logger.info(excluded_str.strip())

        logger.info(f"commands loaded: {len(self.commands)}")

    async def _setup_log_channel(self) -> None:
        if self.log_channel_id is None:
            logger.warning("log channel not set because log channel id was not set")
            self.log_channel = None
            return

        logger.info(f"getting log channel with id {self.log_channel_id}")
        try:
            channel = await self.fetch_channel(self.log_channel_id)

        except Exception as e:
            logger.critical(
                f"could not get log channel with id {self.log_channel_id} due to exception:",
                exc_info=e,
            )

        else:
            if isinstance(channel, discord.TextChannel):
                self.log_channel = channel
            else:
                logger.critical(
                    f"log channel with id {self.log_channel_id} is not a text channel, log_channel not set"
                )

        if not self.log_channel:
            logger.critical(
                f"log channel with id {self.log_channel_id} not found. this can cause problems."
            )
        else:
            logger.info(
                f"log channel: #{self.log_channel.name} (id: {self.log_channel.id})"
            )

    async def setup_hook(self) -> None:
        self.uptime = discord.utils.utcnow()

        assert self.user is not None

        mprint()
        mprint(
            f"{white}~{reset} {bold}{green}{BOT_NAME.upper()}{reset} {white}~{reset}"
        )
        mprint(
            f"{bright_green}running on{reset} {yellow}python{reset} {blue}{sys.version.split()[0]}{reset}; {yellow}discord.py{reset} {blue}{pkg_resources.get_distribution('discord.py').version}{reset}"
        )
        mprint()

        await self.connect_db()
        await self._load_all_cogs()

        await self.tree.update_app_commands()
        logger.info(f"app commands loaded: {len(self.tree.all_app_commands)}")

        logger.info("logged in successfully")
        logger.info(f"user: {self.user} ({self.user.id})")
        logger.info(
            f"invite: https://discord.com/oauth2/authorize?client_id={self.user.id}&permissions=8&scope=bot+applications.commands"
        )

        await self._setup_log_channel()

        try:
            if self.log_channel is not None:
                await self.log_channel.send(
                    f"**{self.user.name}** logged in successfully", silent=True
                )
        except Exception as e:
            logger.critical(
                f"could not send log message to log channel with id {self.log_channel_id} due to exception:",
                exc_info=e,
            )

    async def close(self, *, abandon: bool = False) -> None:
        """Disconnect from the database, close the bot, flush stdout & stderr and shutdown loggers"""
        # Disconnect from the database
        await self.disconnect_db()

        # Close the bot
        await super().close()

        # Flush stdout & stderr
        sys.stdout.flush()
        sys.stderr.flush()

        # Shutdown loggers
        logger.critical(
            "bot process exited" if not abandon else "bot process exited (abandoned)"
        )
        logging.shutdown()

        if abandon:
            print()

    def slash_mention(self, qualified_command_name: str) -> str:
        """Mention an application command like a normal user or channel mention"""
        return self.tree.slash_mention(qualified_command_name)

    async def get_context(
        self, message: discord.Message, *, cls: type["ContextT_co"] = Context
    ) -> "ContextT_co":
        return await super().get_context(message, cls=cls)

    @staticmethod
    async def get_context_from_interaction(
        interaction: discord.Interaction, *, cls: type["ContextT_co"] = Context
    ) -> "ContextT_co":
        """Get Context from a discord.Interaction"""
        return await cls.from_interaction(interaction)
