import utils
from typing import Optional, Literal
from datetime import datetime

import discord
from discord.ext import commands

class Context(commands.Context):
    """Utility class for commands that is used to easily interact with commands."""

    def __init__(self, *args, **kwargs) -> None: # initialize the class
        super().__init__(*args, **kwargs)
        self.voice: Optional[discord.VoiceState] = self.author.voice
        self.cleaned_up_code = utils.cleanup_code(self.message.content)
    
    async def react(self, emoji: discord.Emoji) -> discord.Reaction:
        """Add reaction to a message"""
        return await self.message.add_reaction(emoji)
    
    def create_board(self, title: str = None, description: str = None, url: str = None, timestamp: datetime = None) -> discord.Embed:
        """Return a discord.Embed"""
        return discord.Embed(
            title=title,
            description=description,
            url=url,
            color=0x2b2d31, # Dark Gray Embed Background
            timestamp=timestamp
        )

    async def board(self, title: str = None, description: str = None, url: str = None, timestamp: datetime = None, reply: bool = False) -> discord.Message:
        """Send a board message"""
        board = self.create_board(title, description, url, timestamp)
        if reply:
            return await self.reply(embed=board)
        else:
            return await self.send(embed=board)
    
    async def yes(self) -> discord.Message:          return await self.react("✅")
    async def tick(self) -> discord.Message:         return await self.react("✅")
    async def check(self) -> discord.Message:        return await self.react("✅")
    async def green(self) -> discord.Message:        return await self.react("✅")
    async def success(self) -> discord.Message:      return await self.react("✅")

    async def x(self) -> discord.Message:            return await self.react("❌")
    async def no(self) -> discord.Message:           return await self.react("❌")
    async def red(self) -> discord.Message:          return await self.react("❌")
    async def fail(self) -> discord.Message:         return await self.react("❌")
    async def cross(self) -> discord.Message:        return await self.react("❌")
    async def failure(self) -> discord.Message:      return await self.react("❌")
    async def unsuccessful(self) -> discord.Message: return await self.react("❌")

class Bot(commands.Bot):
    """The main bot class which handles everything, including handling of events, commands, interactions and the bot itself."""

    def __init__(self, command_prefix: str, *args, intents: discord.Intents = discord.Intents.all(), **kwargs) -> None: # initialize the class
        super().__init__(command_prefix=command_prefix, intents=intents, *args, **kwargs)
        # edit the bot
    
    async def get_context(self, message: discord.Message, *, cls: commands.Context = Context) -> Context:
        """Get Context from a discord.Message"""
        return await super().get_context(message, cls=cls)
    
    def create_activity(name: str, type: Literal["playing", "streaming", "listening", "watching"] = "playing", *args, **kwargs) -> discord.Activity:
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