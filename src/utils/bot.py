"""
Bot-related utilities.
"""

import config
from typing  import Optional
from classes import Bot, BasicPrefix

import aiohttp
import discord
from discord.ext import commands

__all__ = (
    "get_prefix",
    "get_raw_content_data"
)

async def get_prefix(bot: Bot, message: discord.Message) -> BasicPrefix:
    """Get the prefix for the bot"""
    prefix = config.DEFAULT_PREFIX
    if config.MENTION_IS_ALSO_PREFIX:
        return commands.when_mentioned_or(prefix)(bot, message)
    else:
        return prefix

async def get_raw_content_data(url: str, *args, session: Optional[aiohttp.ClientSession] = None, **kwargs) -> bytes:
    """Get raw content like files and media as bytes"""
    async def get_with_session(session: aiohttp.ClientSession) -> bytes:
        async with session.get(url, ssl=True if url.lower().startswith("https") else False, *args, **kwargs) as response:
            return await response.content.read()
    
    if session is None:
        async with aiohttp.ClientSession() as session:
            return await get_with_session(session)
    else:
        return await get_with_session(session)