import sys
import pkg_resources
from typing   import (
    TYPE_CHECKING,
    Literal
)
from datetime import datetime

import cogs
import utils
import config
from utils               import mprint
from logger              import logging
from termcolors          import *
from termcolors          import rgb
from classes.context     import Context
from classes.commandtree import CommandTree

if TYPE_CHECKING:
    from classes.custom_types import (
        ContextT_co,
        PrefixType
    )

from prisma import Prisma

import discord
from discord     import app_commands
from discord.ext import commands

__all__ = (
    "Bot",
)

class Bot(commands.Bot):
    """The main bot class which handles everything, including handling of events, commands, interactions, cogs, extensions, etc. and the bot itself."""
    tree: CommandTree
    uptime: datetime | None
    prisma: Prisma
    log_channel: discord.TextChannel | None
    log_channel_id: int
    all_app_commands: dict[str, app_commands.AppCommand]
    
    def __init__(
        self,
        command_prefix: "PrefixType",
        *args,
        intents: discord.Intents = discord.Intents.all(),
        tree_cls: type[app_commands.CommandTree] = CommandTree,
        **kwargs
    ) -> None:
        super().__init__(
            command_prefix = command_prefix,
            intents = intents,
            tree_cls = tree_cls,
            *args,
            **kwargs,
            help_command = commands.DefaultHelpCommand()
        )
        self.uptime = None
        self.prisma = Prisma(auto_register=True)
        
        self.all_commands = {}
        
        self.log_channel_id = config.LOG_CHANNEL
        self.log_channel = None
    
    async def connect_db(self) -> None:
        await self.prisma.connect()
    
    async def disconnect_db(self) -> None:
        await self.prisma.disconnect()
    
    async def setup_hook(self) -> None:
        self.uptime = discord.utils.utcnow()
        
        mprint()
        mprint(f"{white}~{reset} {bold}{green}{config.BOT_NAME.upper()}{reset} {white}~{reset}")
        mprint(f"{bright_green}running on{reset} {yellow}python{reset} {blue}{sys.version.split()[0]}{reset}; {yellow}discord.py{reset} {blue}{pkg_resources.get_distribution('discord.py').version}{reset}")
        mprint()
        
        await self.connect_db()
        logging.info("connected to database ./database/database.db")
        
        loaded = []
        excluded = []
        
        exclude = config.COGS_EXCLUDE
        for module in utils.list_modules(cogs):
            if module in exclude or module.replace(cogs.__package__+".", "", 1) in exclude: # pyright: ignore[reportOptionalOperand]
                excluded.append(module + f" {rgb(49, 49, 49)}(excluded in config){reset}")
                continue
            
            try:
                await self.load_extension(module)
            
            except commands.NoEntryPointError:
                logging.warn(f"excluding `{module}` because there is no entry point (no 'setup' function found)")
                excluded.append(module + f" {rgb(49, 49, 49)}(no 'setup' function){reset}")
            
            except Exception as e:
                logging.critical(f"excluding `{module}` because there was an error while loading it (this may cause unintended behaviour)", exc_info=e)
                excluded.append(module + f" {rgb(49, 49, 49)}(error: {e.__class__.__name__}){reset}")
            
            else:
                loaded.append(module)
        
        loaded_paginated = utils.paginate(loaded, 3)
        excluded_paginated = utils.paginate(excluded, 2)
        prefix_length = len(utils.strip_color(logging._prefix_handler("info")))
        
        loaded_str = f"the following cogs have been {underline}loaded{reset}:\n"
        for x in loaded_paginated:
            loaded_str += (" "*prefix_length)+ f"{', '.join(x)}\n"
        
        excluded_str = f"the following cogs have been {underline}excluded{reset}:\n"
        for x in excluded_paginated:
            excluded_str += (" "*prefix_length)+ f"{', '.join(x)}\n"
        
        logging.info(loaded_str.strip())
        logging.info(excluded_str.strip())
        
        logging.info(f"commands loaded: {len(self.commands)}")
        
        if TYPE_CHECKING and self.user is None:
            return  # to satisfy the type checker
        
        await self.update_app_commands()
        logging.info(f"app commands loaded: {len(self.all_app_commands)}")
        
        logging.info("logged in successfully")
        logging.info(f"user: {self.user} ({self.user.id})")
        logging.info(f"invite: https://discord.com/oauth2/authorize?client_id={self.user.id}&permissions=8&scope=bot+applications.commands")
        
        logging.info(f"getting log channel with id {self.log_channel_id}")
        channel = await self.fetch_channel(self.log_channel_id)
        
        if isinstance(channel, discord.TextChannel):
            self.log_channel = channel
        else:
            logging.critical(f"log channel with id {self.log_channel_id} is not a text channel, log_channel not set")
        
        if not self.log_channel:
            logging.critical(f"log channel with id {self.log_channel_id} not found. this can cause problems.")
        else:
            logging.info(f"log channel: #{self.log_channel.name} (id: {self.log_channel.id})")
        
        if TYPE_CHECKING and (
            self.log_channel is None
            or self.user is None
        ):
            # to satisfy the typechecker (aka epic gaslight)
            return
        
        try:
            await self.log_channel.send(f"**{self.user.name}** logged in successfully", silent=True)
        except Exception as e:
            logging.critical(f"could not send log message to log channel with id {self.log_channel_id} due to exception:", exc_info=e)
    
    async def update_app_commands(self) -> None:
        """Update app commands"""
        logging.debug("fetching app commands...")
        self.all_app_commands = {
            cmd.name: cmd
            for cmd in await self.tree.fetch_commands()
        }
        logging.debug(f"app commands fetched ({len(self.all_app_commands)})")
    
    def slash_mention(self, command: str) -> str:
        """Mention an application command like a normal user or channel mention"""
        if command.startswith("/"):
            command = command[1:]
        parent = command.split(maxsplit=1)[0]
        return f"</{command}:{self.all_app_commands[parent].id}>" if self.all_app_commands.get(parent) else f"`/{command}`"
    
    async def get_context(self, message: discord.Message, *, cls: type["ContextT_co"] = Context) -> "ContextT_co":
        """Get Context from a discord.Message"""
        return await super().get_context(message, cls=cls)
    
    @staticmethod
    async def get_context_from_interaction(interaction: discord.Interaction, *, cls: type["ContextT_co"] = Context) -> "ContextT_co":
        """Get Context from a discord.Interaction"""
        return await cls.from_interaction(interaction)
    
    def create_activity(
        self,
        name: str,
        type: Literal["playing", "streaming", "listening", "watching"] = "playing",
        *args,
        **kwargs
    ) -> discord.Activity | discord.Game | discord.Streaming:
        """Create an activity for a given type"""

        match type:
            case "playing":
                return discord.Game(name=name, *args, **kwargs)
            case "streaming":
                return discord.Streaming(name=name, *args, **kwargs)
            case "listening":
                return discord.Activity(type=discord.ActivityType.listening, name=name, *args, **kwargs)
            case "watching":
                return discord.Activity(type=discord.ActivityType.watching, name=name, *args, **kwargs)
