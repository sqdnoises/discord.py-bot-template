from typing import TYPE_CHECKING, Any, Optional, Sequence
from datetime import datetime

from ..utils import cleanup_code

if TYPE_CHECKING:
    from .bot import Bot

import discord
from discord.ext import commands
from discord.utils import MISSING


class Context(commands.Context):
    """Utility class for commands that is used to easily interact with commands."""

    bot: "Bot"
    content: str
    voice: discord.VoiceState | None
    cleaned_up_code: str
    out: bool = True

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.content = self.message.content
        self.voice = (
            self.author.voice if isinstance(self.author, discord.Member) else None
        )
        self.cleaned_up_code = cleanup_code(self.message.content)

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
                content=content,
                embed=embed,
                attachments=attachments,
                suppress=suppress,
                delete_after=delete_after,
                allowed_mentions=allowed_mentions,
                view=view,
            )

        else:
            return await self.message.edit(
                content=content,
                embeds=embeds,
                attachments=attachments,
                suppress=suppress,
                delete_after=delete_after,
                allowed_mentions=allowed_mentions,
                view=view,
            )

    async def react(
        self, emoji: str | discord.Emoji | discord.PartialEmoji | discord.Reaction
    ) -> None:
        """Add a reaction to the message"""
        await self.message.add_reaction(emoji)

    @discord.utils.copy_doc(react)
    async def add_reaction(
        self, emoji: str | discord.Emoji | discord.PartialEmoji | discord.Reaction
    ) -> None:
        await self.react(emoji)

    async def unreact(
        self,
        emoji: str | discord.Emoji | discord.PartialEmoji | discord.Reaction,
        member: Optional[discord.abc.Snowflake] = None,
    ) -> None:
        """
        Remove a reaction from the message

        If `member` is not provided, `member` defaults to `Context.me`.
        """
        await self.message.remove_reaction(emoji, self.me if member is None else member)

    @discord.utils.copy_doc(unreact)
    async def remove_reaction(
        self,
        emoji: str | discord.Emoji | discord.PartialEmoji | discord.Reaction,
        member: Optional[discord.abc.Snowflake] = None,
    ) -> None:
        await self.unreact(emoji, member)

    def create_board(
        self,
        title: str | None = None,
        description: str | None = None,
        url: str | None = None,
        timestamp: datetime | None = None,
    ) -> discord.Embed:
        """Returns a Dark-mode-flushed embed board"""
        return discord.Embed(
            title=title,
            description=description,
            url=url,
            color=discord.Color.dark_embed(),  # dark gray embed, matching discord's embed background
            timestamp=timestamp,
        )

    async def yes(self) -> None:
        await self.react("✅")

    async def done(self) -> None:
        await self.react("✅")

    async def success(self) -> None:
        await self.react("✅")

    async def x(self) -> None:
        await self.react("❌")

    async def no(self) -> None:
        await self.react("❌")

    async def error(self) -> None:
        await self.react("❌")

    async def failed(self) -> None:
        await self.react("❌")

    async def failure(self) -> None:
        await self.react("❌")
