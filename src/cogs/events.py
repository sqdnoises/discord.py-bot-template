import logging
import discord
from classes import Bot
from discord.ext import commands

class Events(commands.Cog):
    """All bot events"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info("ready to handle commands")

async def setup(bot: Bot) -> None:
    await bot.add_cog(Events(bot))