import logging
import discord
from classes import Bot, Context
from discord.ext import commands

class About(commands.Cog):
    """Bot information"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @commands.command()
    async def template_command(self, ctx: Context):
        await ctx.send("Hi!")
        logging.info("Sent Hi!")

async def setup(bot: Bot) -> None:
    await bot.add_cog(About(bot))