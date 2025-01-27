from typing import (
    TYPE_CHECKING, Any,
    Optional, Sequence
)
from datetime import datetime

from .. import utils

if TYPE_CHECKING:
    from .bot import Bot

import discord
from discord.ext   import commands
from discord.utils import MISSING

class Context(commands.Context):
    """Utility class for commands that is used to easily interact with commands."""
    bot: "Bot"
    voice: discord.VoiceState | None
    cleaned_up_code: str
    out: bool = True
    
    def __init__(
        self,
        *args: Any, 
        **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.voice = self.author.voice if isinstance(self.author, discord.Member) else None
        self.cleaned_up_code = utils.cleanup_code(self.message.content)
    
    async def edit(
        self,
        *,
        content: Optional[str] = MISSING,
        embed: Optional[discord.Embed] = MISSING,
        embeds: Sequence[discord.Embed] = MISSING,
        attachments: Sequence[discord.Attachment | discord.File] = MISSING,
        suppress: bool = False,
        delete_after: Optional[float] = None,
        allowed_mentions: Optional[discord.AllowedMentions] = MISSING,
        view: Optional[discord.ui.View] = MISSING
    ) -> discord.Message:
        """Edit the message"""
        
        if embed is not MISSING:
            return await self.message.edit(
                content = content,
                embed = embed,
                attachments = attachments,
                suppress = suppress,
                delete_after = delete_after,
                allowed_mentions = allowed_mentions,
                view = view
            )
        
        else:
            return await self.message.edit(
                content = content,
                embeds = embeds,
                attachments = attachments,
                suppress = suppress,
                delete_after = delete_after,
                allowed_mentions = allowed_mentions,
                view = view
            )
    
    async def react(self, emoji: str | discord.Emoji) -> None:
        """Add reaction to the message"""
        await self.message.add_reaction(emoji)
    
    def create_board(
        self,
        title:       str      | None = None,
        description: str      | None = None,
        url:         str      | None = None,
        timestamp:   datetime | None = None
    ) -> discord.Embed:
        """Return a discord.Embed"""
        return discord.Embed(
            title = title,
            description = description,
            url = url,
            color = discord.Color.dark_embed(), # dark gray embed background
            timestamp = timestamp
        )
    
    async def yes(self)          -> None: await self.react("✅")
    async def done(self)         -> None: await self.react("✅")
    async def tick(self)         -> None: await self.react("✅")
    async def check(self)        -> None: await self.react("✅")
    async def green(self)        -> None: await self.react("✅")
    async def success(self)      -> None: await self.react("✅")
    async def successful(self)   -> None: await self.react("✅")
    
    async def x(self)            -> None: await self.react("❌")
    async def no(self)           -> None: await self.react("❌")
    async def red(self)          -> None: await self.react("❌")
    async def fail(self)         -> None: await self.react("❌")
    async def cross(self)        -> None: await self.react("❌")
    async def failure(self)      -> None: await self.react("❌")
    async def unsuccessful(self) -> None: await self.react("❌")